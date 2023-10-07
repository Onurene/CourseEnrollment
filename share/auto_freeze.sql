PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS auto_freeze;
CREATE TABLE auto_freeze (
  auto_freeze_flag TEXT NOT NULL
);
INSERT INTO auto_freeze (auto_freeze_flag) VALUES ('FALSE');
COMMIT;