--Create a database - titanonline
sqlite3 titanonline

--Create tables

CREATE TABLE Courses(
 course_name vachar(250),
 Course_code varchar(20),
 course_section integer(10),
 Instructor_name  vachar(250),
 Class_capacity integer,
 Waitlist_capacity integer,
 PRIMARY KEY (Course_code,  course_section)
);

CREATE TABLE CourseEnrollmentDetails(
 Course_code varchar(20),
 course_section integer,
 Enrollment_start_date date,
Enrollment_end_date date,
FOREIGN KEY ( Course_code, course_section ) references Courses(Course_code,  course_section)
);

CREATE TABLE Students(
 Student_id varchar(20),
 Student_name varchar(250),
 Student_email varchar(250),
Student_phone varchar(250),
 Current_level_of_study varchar(250),
PRIMARY KEY (student_id)
);


CREATE TABLE StudentCourseEnrollment(
 Student_id  varchar(20),
Course_name varchar(250),
Course_code varchar(20),
course_section varchar(250),
Course_attendance varchar(1),
Enrollment_status varchar(20)
);

.import --csv courses.csv courses
.import --csv couse_enrollment.csv CourseEnrollmentDetails
.import --csv students.csv Students
.import --csv student_enrollment.csv StudentCourseEnrollment 