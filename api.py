import collections
import contextlib
import logging.config
import sqlite3
import typing

from typing import Optional

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from enrollment_helper import enroll_students_from_waitlist, is_auto_enroll_enabled, get_opening_sections

# class Settings(BaseSettings, env_file=".env", extra="ignore"):
#     database: str
#     logging_config: str

class Student(BaseModel):
    id: int
    first_name: str 
    last_name: str
    email: str

def get_db():
    with contextlib.closing(sqlite3.connect("./var/titanonline.db")) as db:
        db.row_factory = sqlite3.Row
        yield db

def get_logger():
    return logging.getLogger(__name__)

# settings = Settings()
app = FastAPI()



# Getting specific professors by using their id, then finding the courses they 
# teach to then find their current enrollments.

@app.get("/professors/{id}/enrollments")
def get_professor_enrollments(
    id: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM PROFESSORS WHERE id = ? LIMIT 1", (id, ))
    professor = cur.fetchall()

    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found"
        )
    
    cur = db.execute("SELECT * FROM COURSE_SECTION WHERE prof_id = ?", (id,))
    course_sections = cur.fetchall()

    course_sections_li = []

    for course in course_sections:
        course_sections_li.append(course)

    
    enrollment_li = []
    for course in course_sections_li:
        cur = db.execute("SELECT * FROM ENROLLMENTS WHERE section_id = ?", (course['id'],))
        enrollments = cur.fetchall()
        
        enrollment_li.extend(enrollments)

    return {"professor": professor, "enrollments": enrollment_li}


# This api is similar to enrollment api made above. Get the professor id, then go to 
# courses the are teaching to get the course.id, to find the students who dropped 
# the class.

@app.get("/professors/{id}/droplists")
def get_professor_droplists(
    id: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM PROFESSORS WHERE id = ? LIMIT 1", (id,))
    professor = cur.fetchall()

    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found"
        )
    
    cur = db.execute("SELECT * FROM COURSE_SECTION WHERE prof_id = ?", (id,))
    course_sections = cur.fetchall()

    course_sections_li = []

    for course in course_sections:
        course_sections_li.append(course)

    
    droplist_li = []
    for course in course_sections_li:
        cur = db.execute("SELECT * FROM DROPLIST WHERE section_id = ?", (course['id'],))
        droplist = cur.fetchall()
        
        droplist_li.extend(droplist)

    return {"professor": professor, "droplist": droplist_li}


# Now, we must drop the student/s adminsitratively, the professor provide their id
# and their student id that needs to be dropped.
# Inspired by Viditi's code

@app.delete("/professors/{prof_id}/course_section/{section_id}/student/{student_id}/drop")
def drop_student(
    prof_id: int, section_id: int, student_id: int, response: Response, db: sqlite3.Connection = Depends(get_db)
    ):

    cur = db.execute("SELECT * FROM PROFESSORS WHERE id = ?", [prof_id])
    professor = cur.fetchall()

    if professor:
        administrative = True
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found"
        )

    try:
        cur = db.execute("DELETE FROM ENROLLMENTS WHERE student_id=? AND section_id=?", [student_id, section_id])
        db.commit()
        cur = db.execute("DELETE FROM WAITLIST WHERE student_id=? AND section_id=?", [student_id, section_id])
        db.commit()       
        cur = db.execute("INSERT INTO droplist(section_id, student_id, drop_date, administrative) VALUES(?, ?, datetime('now'), ?)", [section_id, student_id, administrative])
        db.commit()

        auto_enroll_enabled = is_auto_enroll_enabled(db)

        if auto_enroll_enabled:        
            enrollment_count = enroll_students_from_waitlist(db, [section_id])

        return {"message": "Student dropped and inserted to droplist."}

    except sqlite3.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_40, detail={"type": type(e)._name__, "msg": str(e)}
        )
