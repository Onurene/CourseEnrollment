PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    -- here we use on delete restrict because a strudent's enrollment status may be important information
    -- and we don't want to delete it if the section is deleted  (eg. to determine if a student is full time)
    section_id INTEGER NOT NULL REFERENCES course_section(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(id),
    enrollment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(section_id, student_id)
);

INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,12345678,'2023-08-21 09:00:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,23456789,'2023-08-22 09:00:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,34567890,'2023-08-23 09:00:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,45678901,'2023-08-24 09:00:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,56789012,'2023-08-25 09:00:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,67890123,'2023-08-21 09:30:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,78901234,'2023-08-27 09:40:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,89012345,'2023-08-21 09:50:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,90123456,'2023-08-25 09:10:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,10123456,'2023-08-21 09:20:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,11123456,'2023-08-24 09:15:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2,12123456,'2023-08-22 09:10:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112364, '2023-08-20 09:00:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112365, '2023-08-21 10:30:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112367, '2023-08-22 14:45:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112368, '2023-08-23 11:20:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112369, '2023-08-24 16:05:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112370, '2023-08-25 13:10:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112371, '2023-08-26 09:30:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112372, '2023-08-27 15:20:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112373, '2023-08-28 10:45:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112374, '2023-08-29 12:55:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112375, '2023-08-30 14:00:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112376, '2023-08-21 16:30:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112378, '2023-08-22 11:15:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112379, '2023-08-23 10:00:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112380, '2023-08-24 13:45:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112381, '2023-08-25 15:55:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112382, '2023-08-26 12:20:00');
INSERT INTO enrollments (section_id, student_id, enrollment_date) VALUES (2, 12112383, '2023-08-27 14:10:00');


COMMIT;