PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS droplist;
CREATE TABLE droplist (
    -- we may need drop data for example for eligibility for a refund so even if a section is deleted we don't want to delete the drop data
    section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    student_id INTEGER NOT NULL REFERENCES student(id),
    drop_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    administrative BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(section_id, student_id)
);

COMMIT;
