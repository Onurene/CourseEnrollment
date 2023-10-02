PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS waitlist;
CREATE TABLE waitlist (
    -- we don't need waitlist data for anything so if a serction is deleted we can delete all the waitlist rows too
    section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE CASCADE ON UPDATE CASCADE,
    student_id INTEGER NOT NULL REFERENCES student(id),
    waitlist_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(section_id, student_id)
);

COMMIT;