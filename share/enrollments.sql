PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    -- here we ue on delete restrict because a strudent's enrollment status may be importanti information
    -- and we don't want to delete it if the section is deleted  (eg. to determine if a student is full time)
    section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    student_id INTEGER NOT NULL REFERENCES student(id),
    enrollment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(section_id, student_id)
);

COMMIT;