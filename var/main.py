
import collections
import contextlib
import logging.config
import sqlite3
import typing

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings






class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str


class students(BaseModel):
    Student_id : int
    Student_name :str
    Student_email : str
    Student_phone :str
    Current_level_of_study :str

class StudentCourseEnrollment(BaseModel):
    Student_id  :str
    Course_name  : str
    Course_code :str
    course_section :str
    Course_attendance :str
    Enrollment_status :str      

class enrollments(BaseModel):
    section_id: int
    student_id: int
    enrollment_date: str

class droplist(BaseModel):
    section_id :int
    student_id:int
    drop_date: str
    administrative: bool


def get_db():
    with contextlib.closing(sqlite3.connect("titanonline.db")) as db:
        db.row_factory = sqlite3.Row
        yield db



app = FastAPI()




@app.get("/classes/")
def list_classes(db: sqlite3.Connection = Depends(get_db)):
    classes = db.execute("SELECT * FROM Course")
    return {"classes": classes.fetchall()}



@app.get("/enrollments/")
def list_enrollment(db: sqlite3.Connection = Depends(get_db)):
    enrollments = db.execute("SELECT * FROM enrollments")
    return {"enrollments": enrollments.fetchall()}


@app.delete("/enrollments/{student_id}/{section_id}",status_code=status.HTTP_200_OK)
def remove_student(
    student_id: int, section_id: int, db:sqlite3.Connection = Depends(get_db)
    
):
    try:
        cur = db.execute("DELETE FROM enrollments WHERE student_id=? AND section_id=?",[student_id,section_id])
        db.commit()
        cur = db.execute  ("INSERT INTO droplist(section_id,student_id,drop_date,administrative) VALUES(?, ?, datetime('now'), FALSE)" ,[section_id,student_id])
        db.commit()
                 
    except sqlite3.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_40, 
            detail={"type": type(e)._name_, "msg": str(e)},


        )
    
    







# @app.delete("/classes/{course_no}",status_code=status.HTTP_200_OK)
# def remove_section(
#     course_no:int , db: sqlite3.Connection = Depends(get_db)
# ):
    
#     cur = db.execute("Select * from course where course_no = ?",[course_no])
#     entry = cur.fetchone()
#     if(not entry):
#         raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail= 'Class Does Not Exist',
#             )
#     try:
#         db.execute(
#             """
#             DELETE FROM course WHERE course_no= ? 
#             """,
#             [course_no])
#         db.commit()
#     except sqlite3.IntegrityError as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_40, 
#             detail={"type": type(e)._name_, "msg": str(e)},
#         )
#     return {'status':"Class Dropped Successfully"}



# app.post("/enrollments/", status_code=status.HTTP_201_CREATED)
# def create_enrollment(
#     enrollment: enrollments, section:course_section, waitlist:waitlist ,response: Response, db: sqlite3.Connection = Depends(get_db)
# ):
#     cur = db.execute("select room_num, room_capacity from course_section where course_num = ?",[section.course_num])
#     room_num, room_capacity = cur.fetchone()

#     # Checking if student is Already enrolled to the course
#     cur = db.execute("Select * from enrollments where section_id= ? and  student_id = ? and enrollment_date <= (datetime('now))",[enrollment.section_id, enrollment.student_id])
#     sameClasses = cur.fetchall()
#     if(sameClasses):
#         raise HTTPException(status_code=409, detail="You are already enrolled") #HTTP status code 409, which stands for "Conflict." 
    
#     # Checking if Class is full then adding student to waitlist
#     if(room_num >= room_capacity):

#         # Checking if student is already on waitList
#         cur = db.execute("Select * from waitlist where section_id = ? and  sudent_id = ?",[waitlist.section_id, waitlist.student_id])
#         alreadyOnWaitlist = cur.fetchall()
#         if(alreadyOnWaitlist):
#             raise HTTPException(status_code=409, detail="You are already on waitlist") #HTTP status code 409, which stands for "Conflict." 
#         # Checking that student is not on more than 3 waitlist (not checked)
#         cur = db.execute("Select * from waitlist where student_id = ?",[waitlist.student_id])
#         moreThanThree = cur.fetchall()
#         if(len(moreThanThree)>3):
#             raise HTTPException(status_code=409, detail="Class is full and You are already on three waitlists so, you can't be placed on a waitlist") #HTTP status code 409, which stands for "Conflict." 
        
#         # Adding to the waitlist if waitlist is not full
#         cur = db.execute("Select * from waitlist where section_id= ?",[waitlist.section_id])
#         entries = cur.fetchall()
#         if(len(entries)>=15):
#             raise HTTPException(status_code=403, detail="Waiting List if full for this class") # Forbidden
#         waitListPosition = len(entries)+1
#         e = dict(waitlist)
#         try:
#             cur = db.execute(
#                 """
#                 INSERT INTO waitlist(section_id,student_id,waitlist_date)
#                 VALUES(?, ?, datetime('now')) 
#                 """,
#                 [waitlist.student_id,waitlist.section_id,waitListPosition]
#             )
#             db.commit()
#         except sqlite3.IntegrityError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail={"type": type(e)._name_, "msg": str(e)},
#             )
#         e["id"] = cur.lastrowid
#         response.headers["Location"] = f"/waitlist/{e['id']}"
#         message = f"Class is full you have been placed on waitlist position {waitListPosition}"
#         # Sagar: new function Checking if student was enrolled earlier
#         raise HTTPException(status_code=400, detail=message)
    




