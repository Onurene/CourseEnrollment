PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS droplist;
CREATE TABLE droplist (
    -- we may need drop data for example for eligibility for a refund so even if a section is deleted we don't want to delete the drop data
    section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(id),
    drop_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    administrative BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(section_id, student_id)
);
INSERT INTO droplist (section_id, student_id, drop_date)
VALUES (2, 65123456, '2023-08-24 09:00:00'),
    (2, 73123456, '2023-08-25 10:00:00'),
    (2, 76123456, '2023-08-27 11:30:00'),
    (2, 68123456, '2023-08-28 09:40:00'),
    (2, 85123456, '2023-08-29 09:50:00');
COMMIT;