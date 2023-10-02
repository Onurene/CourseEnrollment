-- create database
.open titanonline.db

-- write ahead log modE
PRAGMA journal_mode=WAL;
-- enforce fk constraints
PRAGMA foreign_keys=ON;

-- create tables

CREATE TABLE IF NOT EXISTS department (
  code TEXT NOT NULL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS professor (
  id INTEGER NOT NULL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS student (
  id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS course (
  department_code TEXT NOT NULL REFERENCES department(code),
  course_no INTEGER NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  PRIMARY KEY (department_code, course_no)
);

CREATE TABLE IF NOT EXISTS course_section (
  id INTEGER PRIMARY KEY,
  dept_code TEXT NOT NULL,
  course_num INTEGER NOT NULL,
  section_no INTEGER NOT NULL,
  semester TEXT NOT NULL CHECK (semester in ('FA', 'WI', 'SP', 'SU')),
  year INTEGER NOT NULL,
  prof_id INTEGER NOT NULL REFERENCES professor(id),
  room_num INTEGER NOT NULL,
  room_capacity INTEGER NOT NULL,
  course_start_date DATE NOT NULL,
  enrollment_start DATETIME NOT NULL,
  enrollment_end DATETIME NOT NULL,
  UNIQUE(dept_code, course_num, section_no, semester, year),
  FOREIGN KEY (dept_code, course_num) REFERENCES course(department_code, course_no)
);

CREATE TABLE IF NOT EXISTS waitlist (
  section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE CASCADE,
  student_id INTEGER NOT NULL REFERENCES student(id),
  waitlist_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(section_id, student_id)
);

CREATE TABLE IF NOT EXISTS enrollment (
  section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE CASCADE,
  student_id INTEGER NOT NULL REFERENCES student(id),
  enrollment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(section_id, student_id)
);

CREATE TABLE IF NOT EXISTS droplist (
  section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE CASCADE,
  student_id INTEGER NOT NULL REFERENCES student(id),
  drop_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  administrative BOOLEAN NOT NULL DEFAULT FALSE,
  UNIQUE(section_id, student_id)
);

-- seed  the database using csv files

.import --csv data/departments.csv department
.import --csv data/professors.csv professor
.import --csv data/students.csv student
.import --csv data/courses.csv course

--.import --csv data/sections.csv course_section
INSERT INTO course_section
VALUES
    (1, "CPSC", 335, 1,'FA',2023, 1, 100, 30, "2023-08-01", "2023-05-01 10:00:00",  "2023-09-01 10:00:00"),
    (2, "CPSC", 335, 2,'FA',2023, 2, 101, 30, "2023-08-01", "2023-05-01 10:00:00",  "2023-09-01 10:00:00"),
    (3, "CPSC", 481, 1,'SP',2023, 3, 102, 30, "2023-01-15", "2022-11-01 10:00:00",  "2023-02-01 10:00:00"),
    (4, "ECON", 315, 1,'FA',2023, 4, 103, 30, "2023-08-01", "2023-05-01 10:00:00",  "2023-09-01 10:00:00"),
    (5, "ACCT", 301, 1,'FA',2023, 5, 104, 30, "2023-08-01", "2023-05-01 10:00:00",  "2023-09-01 10:00:00");

--.import --csv data/waitlists.csv waitlist
INSERT INTO waitlist
VALUES
  (1, 41, "2023-05-31 10:00:00"),
  (1, 42, "2023-05-25 09:00:00"),
  (1, 43, "2023-05-22 08:00:00"),
  (3, 11, "2023-05-15 10:00:00"),
  (3, 12, "2023-05-16 10:00:00");

--.import --csv data/droplists.csv droplist
INSERT INTO droplist
VALUES
  (1, 44, "2023-05-02 11:00:00", FALSE),
  (1, 45, "2023-05-10 12:10:00", FALSE);

--.import --csv data/enrollments.csv enrollment
INSERT INTO enrollment
VALUES
(1, 11, "2023-05-01 11:00:00"),
(1, 12, "2023-05-01 11:10:00"),
(1, 13, "2023-05-02 12:00:00"),
(1, 14, "2023-05-11 13:00:00"),
(1, 15, "2023-05-13 14:10:00"),
(1, 16, "2023-05-12 15:00:00"),
(1, 17, "2023-05-14 15:30:00"),
(1, 18, "2023-05-12 16:10:00"),
(1, 19, "2023-05-11 17:00:00"),
(1, 20, "2023-05-03 18:10:00"),
(1, 21, "2023-05-05 18:30:00"),
(1, 22, "2023-05-02 16:30:00"),
(1, 23, "2023-05-01 11:40:00"),
(1, 24, "2023-05-01 11:30:00"),
(1, 25, "2023-05-04 12:30:00"),
(1, 26, "2023-05-06 11:45:00"),
(1, 27, "2023-05-08 11:10:00"),
(1, 28, "2023-05-09 12:00:00"),
(1, 29, "2023-05-10 11:00:00"),
(1, 30, "2023-05-11 11:10:00"),
(1, 31, "2023-05-12 12:00:00"),
(1, 32, "2023-05-12 11:00:00"),
(1, 33, "2023-05-11 11:10:00"),
(1, 34, "2023-05-10 12:00:00"),
(1, 35, "2023-05-19 11:00:00"),
(1, 36, "2023-05-18 11:10:00"),
(1, 37, "2023-05-20 12:00:00"),
(1, 38, "2023-05-21 11:00:00"),
(1, 39, "2023-05-10 11:10:00"),
(1, 40, "2023-05-12 12:00:00"),
(3, 16, "2023-05-12 12:00:00"),
(3, 17, "2023-05-11 11:00:00"),
(3, 18, "2023-05-10 11:10:00"),
(3, 19, "2023-05-09 12:00:00"),
(3, 20, "2023-05-05 11:00:00"),
(3, 21, "2023-05-03 11:10:00"),
(3, 22, "2023-05-02 12:40:00"),
(3, 23, "2023-05-01 11:10:00"),
(3, 24, "2023-05-01 11:30:00"),
(3, 25, "2023-05-02 12:05:00"),
(3, 26, "2023-05-01 11:03:00"),
(3, 27, "2023-05-01 11:10:00"),
(3, 28, "2023-05-02 12:00:00"),
(3, 29, "2023-05-10 11:00:00"),
(3, 30, "2023-05-03 11:10:00"),
(3, 31, "2023-05-05 13:00:00"),
(3, 32, "2023-05-06 15:00:00"),
(3, 33, "2023-05-07 17:10:00"),
(3, 34, "2023-05-08 18:00:00"),
(3, 35, "2023-05-03 16:30:00"),
(3, 36, "2023-05-04 11:40:00"),
(3, 37, "2023-05-05 12:50:00"),
(3, 38, "2023-05-06 11:40:00"),
(3, 39, "2023-05-09 11:30:00"),
(3, 40, "2023-05-10 12:20:00"),
(3, 41, "2023-05-14 11:00:00"),
(3, 42, "2023-05-12 11:10:00"),
(3, 43, "2023-05-13 12:18:00"),
(3, 44, "2023-05-11 11:00:00"),
(3, 45, "2023-05-14 11:10:00");

