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
  UNIQUE(department_code, course_no)
);

CREATE TABLE IF NOT EXISTS course_section (
  id INTEGER PRIMARY KEY,
  dept_code INTEGER NOT NULL REFERENCES course(department_code),
  course_num INTEGER NOT NULL REFERENCES course(course_no),
  section_no INTEGER NOT NULL,
  semester TEXT NOT NULL CHECK (semester in ('FA', 'WI', 'SP', 'SU')),
  year INTEGER NOT NULL,
  prof_id INTEGER NOT NULL REFERENCES professor(id),
  room_num INTEGER NOT NULL,
  room_capacity INTEGER NOT NULL,
  UNIQUE(dept_code, course_num, section_no, semester, year)
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
