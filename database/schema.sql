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
  email TEXT NOT NULL
  phone INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS student (
  id INTEGER NOT NULL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS course (
  course_no INTEGER NOT NULL,
  department_code TEXT NOT NULL REFERENCES department(code),
  title TEXT NOT NULL,
  description TEXT,
  PRIMARY KEY(course_no, department_code)
);

CREATE TABLE IF NOT EXISTS course_section (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  section_no INTEGER NOT NULL,
  course_num INTEGER NOT NULL REFERENCES course(course_no),
  prof_id INTEGER NOT NULL REFERENCES professor(id),
  semester TEXT NOT NULL CHECK (semester in ('FA', 'WI', 'SP', 'SU')),
  year INTEGER NOT NULL,
  room_num INTEGER NOT NULL,
  room_capacity INTEGER NOT NULL,
  waitlist_capacity INTEGER NOT NULL,
  UNIQUE(section_no, course_num, semester, year)
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

.import --csv departments.csv department
.import --csv professors.csv professor
.import --csv students.csv student
.import --csv courses.csv course
.import --csv sections.csv section
.import --csv waitlists.csv waitlist
.import --csv droplists.csv droplist
.import --csv enrollments.csv enrollment
