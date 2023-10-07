
import collections
import contextlib
import logging.config
import sqlite3
import typing
from datetime import timedelta, datetime

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str


class enrollments(BaseModel):
    section_id: int
    student_id: int
    enrollment_date: str

def get_db():
    with contextlib.closing(sqlite3.connect("titanonline.db")) as db:
        db.row_factory = sqlite3.Row
        yield db

app = FastAPI()

@app.get("/classes/")
def list_classes(db: sqlite3.Connection = Depends(get_db)):
    classes = db.execute("SELECT c.*, cs.section_no as section_no FROM course c inner join course_section cs  on c.department_code = cs.dept_code and c.course_no = cs.course_num")
    return {"classes": classes.fetchall()}

@app.post("/enrollments/{student_id}/{course_no}/{section_no}")
def enroll_students(student_id, course_no, section_no, db: sqlite3.Connection = Depends(get_db)):
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

    if class_capacity==0:
        # check waitlist capacity
        current_waitlist_capacity = db.execute("SELECT COUNT(*) cnt FROM waitlist where section_id = ? group by section_id",(section_id,)).fetchone()
        current_student_waitlist = db.execute("SELECT COUNT(*) cnt FROM waitlist where section_id = ? and student_id = ? group by section_id,student_id",(section_id,student_id)).fetchone()

        current_waitlist_capacity = current_waitlist_capacity['cnt']
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
    db.execute("UPDATE auto_freeze set auto_freeze_flag = ?",(flag,))
    db.commit()
    return {"status_code ": 200}
