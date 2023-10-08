PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS configs;
CREATE TABLE configs (
  automatic_enrollment INTEGER NOT NULL
);
INSERT INTO configs (automatic_enrollment) VALUES (1);
COMMIT;