PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS course_section;
CREATE TABLE course_section (
  id INTEGER PRIMARY KEY,
  dept_code TEXT NOT NULL,
  course_num INTEGER NOT NULL,
  section_no INTEGER NOT NULL,
  semester TEXT NOT NULL,
  year INTEGER NOT NULL,
  prof_id INTEGER NOT NULL REFERENCES professors(id),
  room_capacity INTEGER NOT NULL,
  current_enrollment INTEGER DEFAULT 0,
  frozen BOOLEAN DEFAULT FALSE,
  UNIQUE (
    dept_code,
    course_num,
    section_no,
    semester,
    year
  ),
  FOREIGN KEY (dept_code, course_num) REFERENCES course(department_code, course_no)
);
-- seed the table
INSERT INTO course_section (
    dept_code,
    course_num,
    section_no,
    semester,
    year,
    prof_id,
    room_num,
    room_capacity
  )
VALUES ('CPSC', 101, 1, 'SU', 2023, 1, 101, 30),
  ('CPSC', 201, 1, 'FA', 2023, 2, 102, 25),
  ('EGEC', 301, 1, 'SU', 2023, 3, 201, 20),
  ('HUM', 101, 1, 'SU', 2023, 7, 401, 25),
  ('HUM', 201, 1, 'SU', 2023, 8, 402, 20),
  ('SOC', 301, 1, 'FA', 2023, 9, 501, 18),
  ('CPSC', 101, 2, 'FA', 2023, 3, 102, 20),
  ('CPSC', 201, 2, 'FA', 2023, 4, 103, 18),
  ('EGEC', 301, 2, 'FA', 2023, 5, 202, 22),
  ('HUM', 101, 2, 'FA', 2023, 7, 402, 25),
  ('HUM', 201, 2, 'FA', 2023, 8, 403, 20),
  ('PHRN', 101, 2, 'FA', 2023, 9, 501, 20);
COMMIT;