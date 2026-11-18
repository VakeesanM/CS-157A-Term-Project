-- Rebuilds the School database from scratch (safe to re-run set_up.py)
DROP DATABASE IF EXISTS School;
CREATE DATABASE School;
USE School;

CREATE TABLE Accounts (
    AccountID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    Role VARCHAR(20) NOT NULL DEFAULT 'Student',
    CHECK (Role IN ('Student', 'Admin'))
);

CREATE TABLE Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    AccountID INT NOT NULL UNIQUE,
    FullName VARCHAR(100) NOT NULL,
    Major VARCHAR(100) NOT NULL,
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Professors (
    ProfessorID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Department VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Courses (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    CourseCode VARCHAR(20) NOT NULL UNIQUE,
    CourseTitle VARCHAR(255) NOT NULL,
    Units INT NOT NULL,
    CHECK (Units > 0)
);

CREATE TABLE Sections (
    SectionID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID INT NOT NULL,
    ProfessorID INT NOT NULL,
    Term VARCHAR(20) NOT NULL,
    Year INT NOT NULL,
    Capacity INT NOT NULL,
    Day VARCHAR(20) NOT NULL,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (ProfessorID) REFERENCES Professors(ProfessorID),
    CHECK (Capacity > 0),
    CHECK (EndTime > StartTime)
);

CREATE TABLE Enrollments (
    EnrollmentID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    SectionID INT NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'ENROLLED',
    Grade VARCHAR(5) NOT NULL DEFAULT 'N/A',
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (SectionID) REFERENCES Sections(SectionID),
    UNIQUE (StudentID, SectionID),
    CHECK (Status IN ('ENROLLED', 'DROPPED', 'COMPLETED'))
);
