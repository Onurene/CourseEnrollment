-- create database
.open titanonline.db

-- use write ahead log mode
PRAGMA journal_mode=WAL;
-- enforce fk constraints
PRAGMA foreign_keys=ON;

-- apply migrations

CREATE TABLE IF NOT EXISTS department (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  building TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS professor (
  id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone INTEGER NOT NULL,
  degree TEXT NOT NULL,
  department_no INTEGER UNIQUE NOT NULL REFERENCES department(id)
);

CREATE TABLE IF NOT EXISTS student (
  id INTEGER NOT NULL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  major_dept_no INTEGER NOT NULL REFERENCES department(id)
);

CREATE TABLE IF NOT EXISTS course (
  course_no INTEGER NOT NULL,
  department_no INTEGER NOT NULL REFERENCES department(id),
  professor_id INTEGER NOT NULL REFERENCES professor(id),
  title TEXT NOT NULL,
  description TEXT,
  PRIMARY KEY(course_no, department_no)
);

CREATE TABLE IF NOT EXISTS section (
  section_no INTEGER NOT NULL,
  course_num INTEGER NOT NULL REFERENCES course(course_no),
  prof_id INTEGER NOT NULL REFERENCES professor(id),
  room_num INTEGER NOT NULL,
  room_capacity INTEGER NOT NULL,
  waitlist_capacity INTEGER NOT NULL,
  UNIQUE(section_no, course_num, prof_id)
);

CREATE TABLE IF NOT EXISTS waitlisting (
  course_num INTEGER NOT NULL REFERENCES section(course_num),
  section_num INTEGER NOT NULL REFERENCES section(section_no),
  student_id INTEGER NOT NULL REFERENCES student(id),
  waitlist_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(course_num, section_num, student_id)
);

CREATE TABLE IF NOT EXISTS enrollment (
  course_num INTEGER NOT NULL REFERENCES section(course_num),
  section_num INTEGER NOT NULL REFERENCES section(section_no),
  student_id INTEGER NOT NULL REFERENCES student(id),
  enrollment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(course_num, section_num, student_id)
);

-- seed  the database using csv files

-- todo: update csv files
-- .import --csv departments.csv department
-- .import --csv professors.csv professor
-- .import --csv students.csv student
-- .import --csv courses.csv course
-- .import --csv sections.csv section
-- .import --csv waitlistings.csv waitlisting
-- .import --csv enrollments.csv enrollment
