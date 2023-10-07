import contextlib
import logging.config
import sqlite3
from typing import Optional
import collections
from datetime import timedelta, datetime

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str

class Course(BaseModel):
    department_code: str
    course_no: int
    title: str
    description: str

class SectionPatch(BaseModel):
    section_no: Optional[int] = None
    prof_id: Optional[int] = None
    room_num: Optional[int] = None
    room_capacity: Optional[int] = None
    course_start_date: Optional[str] = None
    enrollment_start: Optional[str] = None
    enrollment_end: Optional[str] = None

class SectionCreate(BaseModel):
    id: int
    dept_code: str
    course_num: int
    section_no: int
    semester: str
    year: int
    prof_id: int
    room_num: int
    room_capacity: int
    course_start_date: str
    enrollment_start: str
    enrollment_end: str

settings = Settings()
app = FastAPI()

def get_db():
    with contextlib.closing(sqlite3.connect(settings.database)) as db:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        yield db


@app.get("/classes/")
def list_classes(db: sqlite3.Connection = Depends(get_db)):
    """
    List all available classes to the student

    Returns:
    - dict: A dictionary containing the details of the classes
    """

    classes = db.execute("SELECT c.*, cs.section_no as section_no FROM course c inner join course_section cs  on c.department_code = cs.dept_code and c.course_no = cs.course_num")
    return {"classes": classes.fetchall()}

@app.post("/enrollments/{student_id}/{course_no}/{section_no}")
def enroll_students(student_id, course_no, section_no, db: sqlite3.Connection = Depends(get_db)):
    """
    Lets a student enroll into the class

    Returns either of the success messages based on the class room capacity and waitlist capacity
    - student successfully enrolled into the class
    - student successfully waitlisted into the class

    Raises:
    - HTTPException (400): If student tries to enroll outside the enrollment window).
    - HTTPException (400): If student has already enrolled into the class.
    - HTTPException (400): Class and waitlist capacity is full, cannot enroll

    """
    max_enrollment_capacity = 30
    waitlist_capacity = 15
    
    course_dates = db.execute("SELECT course_start_date, strftime('%Y-%m-%d',enrollment_start) as enrollment_start, strftime('%Y-%m-%d',enrollment_end) as enrollment_end FROM course_section where course_num = ? and section_no = ?", (course_no,section_no)).fetchone()
    
    # course_start_date = datetime.strptime(course_dates['course_start_date'],'%Y-%m-%d')
    enrollment_start_date = datetime.strptime(course_dates['enrollment_start'],'%Y-%m-%d')    
    enrollment_end_date = datetime.strptime(course_dates['enrollment_end'],'%Y-%m-%d')    
    
    # enrollments not allowed pre and post enrollment dates as defined in the db
    current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d') , '%Y-%m-%d')
    #if current_date > course_start_date+timedelta(days=7) or current_date<enrollment_start_date:
    if current_date > enrollment_end_date or current_date < enrollment_start_date:
        raise HTTPException(status_code=400, detail='You are trying to enroll outside the enrollment window')
    
    # check for class capacity and waitlist capacity
    room_capacity = db.execute("SELECT room_capacity FROM course_section where course_num = ? and section_no = ?", (course_no,section_no)).fetchone()
    section_id = db.execute("SELECT id FROM course_section where course_num = ? and section_no = ?",(course_no,section_no)).fetchone()
    class_capacity = room_capacity['room_capacity']
    section_id = section_id['id']
    

    if class_capacity>=1 and class_capacity<=max_enrollment_capacity:
        # enrollment possible
        # check if student is already enrolled into section id > then return UNIQUE constraint key violation error
        already_enrolled = db.execute  ("Select count(*) cnt from enrollments where section_id=? and student_id=?" ,(section_id,student_id)).fetchone()
        if already_enrolled['cnt']>0:
            raise HTTPException(status_code = 400, detail = "Student already enrolled in this section")            


        db.execute  ("INSERT INTO enrollments(section_id,student_id,enrollment_date) VALUES(?, ?, datetime('now'))" ,(section_id,student_id))
        # decrement room capactity
        db.execute("UPDATE course_section set room_capacity = room_capacity-1 where id = ?",(section_id,))
        db.commit()
        response = f"Student {student_id} enrolled successfully for section_id {section_id}, course_no {course_no},section_no {section_no}"

    elif class_capacity==0:
        # check waitlist capacity
        current_waitlist_capacity = db.execute("SELECT COUNT(*) cnt FROM waitlist where section_id = ? group by section_id",(section_id,)).fetchone()
        current_student_waitlist = db.execute("SELECT COUNT(*) cnt FROM waitlist where section_id = ? and student_id = ? group by section_id,student_id",(section_id,student_id)).fetchone()

        current_waitlist_capacity = current_waitlist_capacity['cnt']
        current_student_waitlist = current_student_waitlist['cnt']
        if current_waitlist_capacity < waitlist_capacity and current_student_waitlist<3:
            #push student in waitlist table
            db.execute  ("INSERT INTO waitlist(section_id,student_id,waitlist_date) VALUES(?, ?, datetime('now'))" ,(section_id,student_id))
            db.commit()
            response = f"Student {student_id} waitlisted successfully for {section_id},{course_no},{section_no}"
        else:
            # enrollment not possible
            raise HTTPException(status_code = 400, detail = "Class capacity and waitlist is full, cannot enroll currently")

    return {"enrollments": response}


@app.post("/freezeenrollment/{flag}")
def freeze_auto_enrollment(flag, db: sqlite3.Connection = Depends(get_db)):
    db.execute("UPDATE configs set automatic_enrollment = ?",(flag,))
    db.commit()
    return {"status_code ": 200}
