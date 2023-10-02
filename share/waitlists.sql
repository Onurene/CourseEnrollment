PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS waitlist;
CREATE TABLE waitlist (
    -- we don't need waitlist data for anything so if a serction is deleted we can delete all the waitlist rows too
    section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE CASCADE ON UPDATE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(id),
    waitlist_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(section_id, student_id)
);
INSERT INTO waitlist (section_id, student_id, waitlist_date) VALUES (2,65123456,'2023-08-28 09:00:00');
INSERT INTO waitlist (section_id, student_id, waitlist_date) VALUES (2,73123456,'2023-08-28 10:00:00');
INSERT INTO waitlist (section_id, student_id, waitlist_date) VALUES (2,76123456,'2023-08-28 11:30:00');
INSERT INTO waitlist (section_id, student_id, waitlist_date) VALUES (2,68123456,'2023-08-29 09:40:00');
INSERT INTO waitlist (section_id, student_id, waitlist_date) VALUES (2,85123456,'2023-08-29 09:50:00');
COMMIT;