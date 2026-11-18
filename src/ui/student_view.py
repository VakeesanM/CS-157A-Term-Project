import streamlit as st

from backend import student as db
from backend.settings import CURRENT_TERM, CURRENT_YEAR
from ui.common import flash, show_flash, section_label


def render_student(account_id):
    if not st.session_state.get("StudentID"):
        st.session_state.StudentID = db.get_student_id(account_id)
    student_id = st.session_state.StudentID
    if student_id is None:
        st.error("No student record is linked to this account.")
        return

    profile = db.get_student_profile(student_id)
    st.subheader(f"Welcome, {profile['FullName']}")
    st.caption(f"{profile['Major']} · {profile['Email']} · Registering for {CURRENT_TERM} {CURRENT_YEAR}")
    show_flash()

    search_tab, classes_tab, history_tab = st.tabs(["Search & Register", "My Classes", "Academic History"])

    with search_tab:
        _search_and_register(student_id)
    with classes_tab:
        _my_classes(student_id)
    with history_tab:
        _history(student_id)


def _search_and_register(student_id):
    col1, col2, col3 = st.columns([2, 2, 1])
    keyword = col1.text_input("Course code or title", placeholder="e.g. CS 157A or Database")
    professor = col2.text_input("Professor", placeholder="e.g. Ivanov")
    day = col3.selectbox("Days", ["Any", "MW", "TR", "F"])

    results = db.search(keyword, professor, "" if day == "Any" else day)
    if not results:
        st.info("No sections match your search.")
        return

    st.dataframe(
        [{"Section": r["SectionID"], "Course": r["CourseCode"], "Title": r["CourseTitle"],
          "Units": r["Units"], "Professor": r["Professor"], "Days": r["Day"],
          "Time": f"{r['StartTime']} – {r['EndTime']}", "Seats Left": r["SeatsLeft"]}
         for r in results],
        hide_index=True, width="stretch",
    )

    open_sections = [r for r in results if r["SeatsLeft"] > 0]
    if not open_sections:
        st.warning("Every section in these results is full.")
        return

    choice = st.selectbox("Pick a section to register for", open_sections, format_func=section_label)
    if st.button("Register", type="primary"):
        ok, message = db.enroll(student_id, choice["SectionID"])
        flash("success" if ok else "error", message)
        st.rerun()


def _my_classes(student_id):
    classes = db.current_classes(student_id)
    if not classes:
        st.info(f"You are not enrolled in any {CURRENT_TERM} {CURRENT_YEAR} classes yet.")
        return

    total_units = sum(c["Units"] for c in classes)
    st.metric("Units this term", total_units)
    st.dataframe(
        [{"Section": c["SectionID"], "Course": c["CourseCode"], "Title": c["CourseTitle"],
          "Units": c["Units"], "Professor": c["Professor"], "Days": c["Day"],
          "Time": f"{c['StartTime']} – {c['EndTime']}"} for c in classes],
        hide_index=True, width="stretch",
    )

    to_drop = st.selectbox("Drop a class", classes, format_func=section_label)
    confirm = st.checkbox("I understand dropping removes me from this section.")
    if st.button("Drop class", disabled=not confirm):
        ok, message = db.drop(student_id, to_drop["SectionID"])
        flash("success" if ok else "error", message)
        st.rerun()


def _history(student_id):
    history = db.view_history(student_id)
    if not history:
        st.info("No past enrollments yet.")
        return

    completed_units = sum(h["Units"] for h in history if h["Status"] == "COMPLETED")
    gpa = db.gpa(history)
    col1, col2 = st.columns(2)
    col1.metric("Units completed", completed_units)
    col2.metric("GPA", gpa if gpa is not None else "N/A")

    st.dataframe(
        [{"Term": f"{h['Term']} {h['Year']}", "Course": h["CourseCode"], "Title": h["CourseTitle"],
          "Units": h["Units"], "Professor": h["Professor"], "Status": h["Status"], "Grade": h["Grade"]}
         for h in history],
        hide_index=True, width="stretch",
    )
