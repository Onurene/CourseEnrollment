PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (code TEXT PRIMARY KEY, name TEXT NOT NULL);
INSERT INTO departments(code, name)
VALUES ('CPSC', 'Computer Science'),
  ('EGEC', 'Computer Engineering'),
  ('EGEE', 'Electrical Engineering'),
  ('HUM', 'Humanities'),
  ('SOC', 'Sociology'),
  ('PSYC', 'Psychology'),
  ('PHRN', 'Phrenology');
COMMIT;