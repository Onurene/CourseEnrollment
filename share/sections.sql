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
  room_num INTEGER NOT NULL,
  room_capacity INTEGER NOT NULL,
  course_start_date TEXT NOT NULL,
  enrollment_start TEXT NOT NULL,
  enrollment_end TEXT NOT NULL,
  UNIQUE (
    dept_code,
    course_num,
    section_no,
    semester,
    year
  ),
  FOREIGN KEY (dept_code, course_num) REFERENCES course(department_code, course_no)
);
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (1, 'CPSC', 101, 1, 'SU', 2023, 1, 101, 30, '2023-06-12', '2023-06-01 09:00:00', '2023-06-15 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (2, 'CPSC', 201, 1, 'FA', 2023, 2, 102, 25, '2023-09-05', '2023-08-20 09:00:00', '2023-09-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (3, 'EGEC', 301, 1, 'SU', 2023, 3, 201, 20, '2023-06-12', '2023-05-30 09:00:00', '2023-06-15 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (4, 'EGEE', 401, 1, 'FA', 2023, 4, 202, 15, '2023-09-05', '2023-08-20 09:00:00', '2023-09-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (5, 'HUM', 101, 1, 'SU', 2023, 7, 401, 25, '2023-06-12', '2023-05-30 09:00:00', '2023-06-15 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (6, 'HUM', 201, 1, 'SU', 2023, 8, 402, 20, '2023-06-12', '2023-05-30 09:00:00', '2023-06-15 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (7, 'SOC', 301, 1, 'FA', 2023, 9, 501, 18, '2023-09-05', '2023-08-20 09:00:00', '2023-09-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (8, 'PHRN', 101, 1, 'SU', 2023, 10, 601, 20, '2023-06-12', '2023-05-30 09:00:00', '2023-06-15 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (9, 'CPSC', 101, 2, 'FA', 2023, 3, 102, 20, '2023-09-05', '2023-08-20 09:00:00', '2023-09-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (10, 'CPSC', 201, 2, 'FA', 2023, 4, 103, 18, '2023-09-05', '2023-08-20 09:00:00', '2023-09-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (11, 'EGEC', 301, 2, 'FA', 2023, 5, 202, 22, '2023-09-05', '2023-08-20 09:00:00', '2023-09-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (12, 'EGEE', 401, 2, 'FA', 2023, 6, 203, 15, '2023-09-05', '2023-08-20 09:00:00', '2023-09-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (13, 'HUM', 101, 2, 'FA', 2023, 7, 402, 25, '2023-09-05', '2023-08-20 09:00:00', '2023-09-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (14, 'HUM', 201, 2, 'FA', 2023, 8, 403, 20, '2023-10-05', '2023-10-01 09:00:00', '2023-10-25 17:00:00');
INSERT INTO course_section (id, dept_code, course_num, section_no, semester, year, prof_id, room_num, room_capacity, course_start_date, enrollment_start, enrollment_end) VALUES (15, 'PHRN', 101, 2, 'FA', 2023, 9, 501, 20, '2023-10-05', '2023-10-01 09:00:00', '2023-10-25 17:00:00');
COMMIT;
