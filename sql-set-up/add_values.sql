-- Sample data: at least 15 rows in every table.
-- Accounts are created (with hashed passwords) by set_up.py before this file runs,
-- so Students look up their AccountID by email instead of hard-coding IDs.
-- Current registration term is Spring 2027; Fall 2026 sections are past terms.

INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Emma Johnson', 'Computer Science' FROM Accounts WHERE Email = 'emma.johnson@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Liam Smith', 'Data Science' FROM Accounts WHERE Email = 'liam.smith@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Olivia Garcia', 'Software Engineering' FROM Accounts WHERE Email = 'olivia.garcia@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Noah Martinez', 'Mathematics' FROM Accounts WHERE Email = 'noah.martinez@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Ava Brown', 'Computer Science' FROM Accounts WHERE Email = 'ava.brown@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Ethan Davis', 'Data Science' FROM Accounts WHERE Email = 'ethan.davis@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Sophia Lopez', 'Computer Science' FROM Accounts WHERE Email = 'sophia.lopez@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Mason Wilson', 'Software Engineering' FROM Accounts WHERE Email = 'mason.wilson@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Isabella Clark', 'Mathematics' FROM Accounts WHERE Email = 'isabella.clark@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Lucas Young', 'Computer Science' FROM Accounts WHERE Email = 'lucas.young@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Justin Young', 'Data Science' FROM Accounts WHERE Email = 'justin.young@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Preston Smit', 'Computer Science' FROM Accounts WHERE Email = 'preston.smit@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Harper Lee', 'Software Engineering' FROM Accounts WHERE Email = 'harper.lee@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Jacob Nguyen', 'Data Science' FROM Accounts WHERE Email = 'jacob.nguyen@school.edu';
INSERT INTO Students (AccountID, FullName, Major)
SELECT AccountID, 'Mia Patel', 'Mathematics' FROM Accounts WHERE Email = 'mia.patel@school.edu';

INSERT INTO Professors (FullName, Department, Email) VALUES
('Alan Reyes', 'Computer Science', 'alan.reyes@school.edu'),
('Beatrice Kim', 'Computer Science', 'beatrice.kim@school.edu'),
('Carlos Mendez', 'Computer Science', 'carlos.mendez@school.edu'),
('Diana Okafor', 'Computer Engineering', 'diana.okafor@school.edu'),
('Edward Chang', 'Computer Science', 'edward.chang@school.edu'),
('Fatima Haddad', 'Computer Science', 'fatima.haddad@school.edu'),
('George Ivanov', 'Computer Science', 'george.ivanov@school.edu'),
('Hannah Schultz', 'Computer Science', 'hannah.schultz@school.edu'),
('Isaac Romero', 'Computer Science', 'isaac.romero@school.edu'),
('Julia Bennett', 'Mathematics', 'julia.bennett@school.edu'),
('Kevin Sato', 'Mathematics', 'kevin.sato@school.edu'),
('Laura Fischer', 'Mathematics', 'laura.fischer@school.edu'),
('Miguel Alvarez', 'Mathematics and Statistics', 'miguel.alvarez@school.edu'),
('Nina Kapoor', 'Data Science', 'nina.kapoor@school.edu'),
('Oscar Grant', 'English', 'oscar.grant@school.edu');

INSERT INTO Courses (CourseCode, CourseTitle, Units) VALUES
('CS 46A', 'Introduction to Programming', 4),
('CS 46B', 'Introduction to Data Structures', 4),
('CS 146', 'Data Structures and Algorithms', 3),
('CS 147', 'Computer Architecture', 3),
('CS 149', 'Operating Systems', 3),
('CS 151', 'Object-Oriented Design', 3),
('CS 157A', 'Introduction to Database Management Systems', 3),
('CS 156', 'Introduction to Artificial Intelligence', 3),
('CS 160', 'Software Engineering', 3),
('MATH 30', 'Calculus I', 3),
('MATH 42', 'Discrete Mathematics', 3),
('MATH 129A', 'Linear Algebra I', 3),
('MATH 161A', 'Applied Probability and Statistics I', 3),
('DATA 220', 'Mathematical Methods for Data Analysis', 3),
('ENGL 1A', 'First-Year Writing', 3);

-- SectionIDs 1-5: Fall 2026 (past). SectionIDs 6-18: Spring 2027 (current).
-- Section 12 (CS 156) has capacity 2 and is full, to demo the capacity check.
-- Section 18 (MATH 42, TR 09:00) overlaps section 7 (CS 147, TR 09:00), to demo the time-conflict check.
INSERT INTO Sections (CourseID, ProfessorID, Term, Year, Capacity, Day, StartTime, EndTime) VALUES
(1, 1, 'Fall', 2026, 30, 'MW', '09:00:00', '10:15:00'),
(10, 10, 'Fall', 2026, 30, 'TR', '10:30:00', '11:45:00'),
(11, 11, 'Fall', 2026, 30, 'MW', '12:00:00', '13:15:00'),
(2, 2, 'Fall', 2026, 30, 'TR', '13:30:00', '14:45:00'),
(15, 15, 'Fall', 2026, 25, 'F', '09:00:00', '11:45:00'),
(3, 3, 'Spring', 2027, 35, 'MW', '09:00:00', '10:15:00'),
(4, 4, 'Spring', 2027, 35, 'TR', '09:00:00', '10:15:00'),
(5, 5, 'Spring', 2027, 30, 'MW', '10:30:00', '11:45:00'),
(6, 6, 'Spring', 2027, 30, 'TR', '10:30:00', '11:45:00'),
(7, 7, 'Spring', 2027, 40, 'MW', '13:30:00', '14:45:00'),
(7, 8, 'Spring', 2027, 40, 'TR', '15:00:00', '16:15:00'),
(8, 8, 'Spring', 2027, 2, 'MW', '15:00:00', '16:15:00'),
(9, 9, 'Spring', 2027, 30, 'F', '10:00:00', '12:45:00'),
(12, 12, 'Spring', 2027, 30, 'TR', '12:00:00', '13:15:00'),
(13, 13, 'Spring', 2027, 30, 'MW', '12:00:00', '13:15:00'),
(14, 14, 'Spring', 2027, 25, 'TR', '18:00:00', '19:15:00'),
(1, 1, 'Spring', 2027, 30, 'MW', '18:00:00', '19:15:00'),
(11, 11, 'Spring', 2027, 30, 'TR', '09:00:00', '10:15:00');

INSERT INTO Enrollments (StudentID, SectionID, Status, Grade) VALUES
(1, 1, 'COMPLETED', 'A'),
(1, 2, 'COMPLETED', 'A-'),
(2, 1, 'COMPLETED', 'B+'),
(2, 3, 'COMPLETED', 'B'),
(3, 4, 'COMPLETED', 'A'),
(3, 5, 'COMPLETED', 'A-'),
(4, 2, 'COMPLETED', 'C+'),
(5, 3, 'COMPLETED', 'B-'),
(6, 4, 'COMPLETED', 'A'),
(7, 5, 'COMPLETED', 'B+'),
(8, 1, 'COMPLETED', 'A-'),
(9, 3, 'DROPPED', 'N/A'),
(1, 10, 'ENROLLED', 'N/A'),
(1, 6, 'ENROLLED', 'N/A'),
(2, 12, 'ENROLLED', 'N/A'),
(3, 12, 'ENROLLED', 'N/A'),
(4, 7, 'ENROLLED', 'N/A'),
(5, 10, 'ENROLLED', 'N/A'),
(6, 8, 'ENROLLED', 'N/A'),
(10, 11, 'ENROLLED', 'N/A'),
(11, 13, 'ENROLLED', 'N/A'),
(13, 15, 'ENROLLED', 'N/A'),
(14, 16, 'ENROLLED', 'N/A');
