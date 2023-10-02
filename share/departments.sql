PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
  code TEXT PRIMARY KEY,
  name TEXT NOT NULL
);
INSERT INTO departments(code, name) VALUES('CPSC', 'Computer Science');
INSERT INTO departments(code, name) VALUES('EGEC', 'Computer Engineering');
INSERT INTO departments(code, name) VALUES('EGEE', 'Electrical Engineering');
INSERT INTO departments(code, name) VALUES('HUM', 'Humanities');
INSERT INTO departments(code, name) VALUES('SOC', 'Sociology');
INSERT INTO departments(code, name) VALUES('PSYC', 'Psychology');
INSERT INTO departments(code, name) VALUES('PHRN', 'Phrenology');
COMMIT;
