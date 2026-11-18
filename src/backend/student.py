"""Student-side database functions.

Every function opens its own connection, runs parameterized SQL through
mysql-connector-python (no ORM), and closes the connection.
"""
from mysql.connector import Error, IntegrityError

from backend.connection import create_connection
from backend.settings import CURRENT_TERM, CURRENT_YEAR

GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0,
}


# ---------- helpers ----------

def format_time(value):
    """MySQL TIME comes back as a timedelta; turn it into '9:00 AM'."""
    total_minutes = int(value.total_seconds()) // 60
    hours, minutes = divmod(total_minutes, 60)
    suffix = "AM" if hours < 12 else "PM"
    hours = hours % 12 or 12
    return f"{hours}:{minutes:02d} {suffix}"


def _times_overlap(a, b):
    """True if two sections meet on a shared day at overlapping times."""
    shares_day = any(day in b["Day"] for day in a["Day"])
    return shares_day and a["StartTime"] < b["EndTime"] and b["StartTime"] < a["EndTime"]


def _format_rows(rows):
    for row in rows:
        for key in ("StartTime", "EndTime"):
            if key in row and row[key] is not None:
                row[key] = format_time(row[key])
    return rows


# ---------- lookups ----------

def get_student_id(account_id):
    """Map a logged-in AccountID to its StudentID (None for admins)."""
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT StudentID FROM Students WHERE AccountID = %s", (account_id,))
            row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def get_student_profile(student_id):
    """Name, major and email for the student header (never the password hash)."""
    query = """
        SELECT s.StudentID, s.FullName, s.Major, a.Email
        FROM Students s
        JOIN Accounts a ON a.AccountID = s.AccountID
        WHERE s.StudentID = %s
    """
    conn = create_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (student_id,))
            return cursor.fetchone()
    finally:
        conn.close()


# ---------- search ----------

def search(keyword="", professor="", day="", term=CURRENT_TERM, year=CURRENT_YEAR):
    """Search sections by course code/title, professor and day.

    Returns one dict per section with SeatsLeft = Capacity - ENROLLED count.
    """
    query = """
        SELECT s.SectionID, c.CourseCode, c.CourseTitle, c.Units,
               p.FullName AS Professor, s.Term, s.Year, s.Day,
               s.StartTime, s.EndTime, s.Capacity,
               s.Capacity - COUNT(e.EnrollmentID) AS SeatsLeft
        FROM Sections s
        JOIN Courses c ON c.CourseID = s.CourseID
        JOIN Professors p ON p.ProfessorID = s.ProfessorID
        LEFT JOIN Enrollments e ON e.SectionID = s.SectionID AND e.Status = 'ENROLLED'
        WHERE s.Term = %s AND s.Year = %s
          AND (c.CourseCode LIKE %s OR c.CourseTitle LIKE %s)
          AND p.FullName LIKE %s
          AND s.Day LIKE %s
        GROUP BY s.SectionID, c.CourseCode, c.CourseTitle, c.Units, p.FullName,
                 s.Term, s.Year, s.Day, s.StartTime, s.EndTime, s.Capacity
        ORDER BY c.CourseCode, s.SectionID
    """
    pattern = f"%{keyword.strip()}%"
    params = (term, year, pattern, pattern, f"%{professor.strip()}%", f"%{day.strip()}%")
    conn = create_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            return _format_rows(cursor.fetchall())
    finally:
        conn.close()


# ---------- capacity ----------

def can_enroll(section_id):
    """True if the section still has open seats."""
    query = """
        SELECT s.Capacity, COUNT(e.EnrollmentID)
        FROM Sections s
        LEFT JOIN Enrollments e ON e.SectionID = s.SectionID AND e.Status = 'ENROLLED'
        WHERE s.SectionID = %s
        GROUP BY s.SectionID, s.Capacity
    """
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (section_id,))
            row = cursor.fetchone()
        return bool(row) and row[1] < row[0]
    finally:
        conn.close()


# ---------- enroll / drop ----------

def enroll(student_id, section_id):
    """Enroll a student in a current-term section.

    Runs as one transaction. SELECT ... FOR UPDATE locks the section row, so two
    students can't both take the last seat at the same time.
    Returns (success: bool, message: str).
    """
    conn = create_connection()
    try:
        conn.start_transaction()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT SectionID, CourseID, Capacity, Term, Year, Day, StartTime, EndTime "
                "FROM Sections WHERE SectionID = %s FOR UPDATE",
                (section_id,),
            )
            section = cursor.fetchone()
            if not section:
                conn.rollback()
                return False, "That section does not exist."
            if (section["Term"], section["Year"]) != (CURRENT_TERM, CURRENT_YEAR):
                conn.rollback()
                return False, f"You can only register for {CURRENT_TERM} {CURRENT_YEAR} sections."

            cursor.execute(
                "SELECT EnrollmentID, Status FROM Enrollments "
                "WHERE StudentID = %s AND SectionID = %s FOR UPDATE",
                (student_id, section_id),
            )
            existing = cursor.fetchone()
            if existing and existing["Status"] == "ENROLLED":
                conn.rollback()
                return False, "You are already enrolled in this section."
            if existing and existing["Status"] == "COMPLETED":
                conn.rollback()
                return False, "You already completed this section."

            # Other sections this student is taking this term
            cursor.execute(
                "SELECT s.SectionID, s.CourseID, s.Day, s.StartTime, s.EndTime, c.CourseCode "
                "FROM Enrollments e "
                "JOIN Sections s ON s.SectionID = e.SectionID "
                "JOIN Courses c ON c.CourseID = s.CourseID "
                "WHERE e.StudentID = %s AND e.Status = 'ENROLLED' AND s.Term = %s AND s.Year = %s",
                (student_id, CURRENT_TERM, CURRENT_YEAR),
            )
            current = cursor.fetchall()
            for other in current:
                if other["CourseID"] == section["CourseID"]:
                    conn.rollback()
                    return False, f"You are already enrolled in another section of {other['CourseCode']}."
                if _times_overlap(section, other):
                    conn.rollback()
                    return False, f"Time conflict with {other['CourseCode']} (section {other['SectionID']})."

            cursor.execute(
                "SELECT COUNT(*) AS Taken FROM Enrollments WHERE SectionID = %s AND Status = 'ENROLLED'",
                (section_id,),
            )
            if cursor.fetchone()["Taken"] >= section["Capacity"]:
                conn.rollback()
                return False, "This section is full."

            if existing:  # previously DROPPED -> re-activate the same row (UNIQUE(StudentID, SectionID))
                cursor.execute(
                    "UPDATE Enrollments SET Status = 'ENROLLED', Grade = 'N/A' WHERE EnrollmentID = %s",
                    (existing["EnrollmentID"],),
                )
            else:
                cursor.execute(
                    "INSERT INTO Enrollments (StudentID, SectionID, Status, Grade) "
                    "VALUES (%s, %s, 'ENROLLED', 'N/A')",
                    (student_id, section_id),
                )
        conn.commit()
        return True, "Enrolled successfully."
    except IntegrityError:
        conn.rollback()
        return False, "You are already enrolled in this section."
    except Error as err:
        conn.rollback()
        return False, f"Database error: {err.msg}"
    finally:
        conn.close()


def drop(student_id, section_id):
    """Drop a current-term class. Updates Status to DROPPED instead of deleting the row."""
    query = """
        UPDATE Enrollments e
        JOIN Sections s ON s.SectionID = e.SectionID
        SET e.Status = 'DROPPED'
        WHERE e.StudentID = %s AND e.SectionID = %s AND e.Status = 'ENROLLED'
          AND s.Term = %s AND s.Year = %s
    """
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (student_id, section_id, CURRENT_TERM, CURRENT_YEAR))
            changed = cursor.rowcount
        conn.commit()
        if changed == 0:
            return False, "You are not enrolled in that section this term."
        return True, "Class dropped."
    except Error as err:
        conn.rollback()
        return False, f"Database error: {err.msg}"
    finally:
        conn.close()


# ---------- schedule and history ----------

def current_classes(student_id):
    """The student's ENROLLED sections for the current term."""
    query = """
        SELECT s.SectionID, c.CourseCode, c.CourseTitle, c.Units, p.FullName AS Professor,
               s.Day, s.StartTime, s.EndTime
        FROM Enrollments e
        JOIN Sections s ON s.SectionID = e.SectionID
        JOIN Courses c ON c.CourseID = s.CourseID
        JOIN Professors p ON p.ProfessorID = s.ProfessorID
        WHERE e.StudentID = %s AND e.Status = 'ENROLLED' AND s.Term = %s AND s.Year = %s
        ORDER BY s.Day, s.StartTime
    """
    conn = create_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (student_id, CURRENT_TERM, CURRENT_YEAR))
            return _format_rows(cursor.fetchall())
    finally:
        conn.close()


def view_history(student_id):
    """Past enrollments (completed and dropped) with grades, newest term first."""
    query = """
        SELECT s.Term, s.Year, c.CourseCode, c.CourseTitle, c.Units,
               p.FullName AS Professor, e.Status, e.Grade
        FROM Enrollments e
        JOIN Sections s ON s.SectionID = e.SectionID
        JOIN Courses c ON c.CourseID = s.CourseID
        JOIN Professors p ON p.ProfessorID = s.ProfessorID
        WHERE e.StudentID = %s
          AND (e.Status = 'COMPLETED' OR NOT (s.Term = %s AND s.Year = %s))
        ORDER BY s.Year DESC, FIELD(s.Term, 'Fall', 'Summer', 'Spring'), c.CourseCode
    """
    conn = create_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (student_id, CURRENT_TERM, CURRENT_YEAR))
            return cursor.fetchall()
    finally:
        conn.close()


def gpa(history_rows):
    """Unit-weighted GPA from view_history() rows (COMPLETED rows with letter grades only)."""
    points = units = 0
    for row in history_rows:
        if row["Status"] == "COMPLETED" and row["Grade"] in GRADE_POINTS:
            points += GRADE_POINTS[row["Grade"]] * row["Units"]
            units += row["Units"]
    return round(points / units, 2) if units else None
