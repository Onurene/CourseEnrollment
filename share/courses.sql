PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS course;
CREATE TABLE course (
  department_code TEXT NOT NULL REFERENCES departments(code),
  course_no INTEGER NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  PRIMARY KEY (department_code, course_no)
);
INSERT INTO course (department_code, course_no, title, description)
VALUES (
    'CPSC',
    101,
    'Introduction to Computer Science',
    'Overview of fundamental concepts in computer science.'
  ),
  (
    'CPSC',
    201,
    'Data Structures and Algorithms',
    'Study of common data structures and algorithms.'
  ),
  (
    'EGEC',
    301,
    'Digital Circuits',
    'Introduction to digital circuit design and analysis.'
  ),
  (
    'EGEE',
    401,
    'Electromagnetic Fields and Waves',
    'Fundamental principles of electromagnetic fields and waves.'
  ),
  (
    'HUM',
    101,
    'Introduction to Literature',
    'Exploration of literary genres and analysis.'
  ),
  (
    'HUM',
    201,
    'World History',
    'Survey of world history from ancient times to the present.'
  ),
  (
    'SOC',
    301,
    'Sociological Theories',
    'Overview of major sociological theories and their applications.'
  ),
  (
    'PHRN',
    101,
    'Introduction to Phrenology',
    'Historical and contemporary overview of phrenology, the most comprehensive and accurate science of human behavior and the brain.'
  );
COMMIT;