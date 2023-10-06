import collections
import contextlib
import logging.config
import sqlite3
import typing

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings


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


# logging.config.fileConfig(settings.logging_config, disable_existing_loggers=False)

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

@app.delete("/professors/{prof_id}/student/{student_id}/drop")
def drop_student(
    prof_id: int, student_id: int, response: Response, db: sqlite3.Connection = Depends(get_db)
    ):
    cur = db.execute("SELECT * FROM PROFESSORS WHERE id = ?", [prof_id])
    professor = cur.fetchall()

    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found"
        )

    # Go through the course_sections the professor is teaching to find the student in
    # either enrollment or waitlist tables.
    cur = db.execute("SELECT * FROM COURSE_SECTION WHERE prof_id = ?", [prof_id])
    course_sections = cur.fetchall()

    for course in course_sections:
        enroll_cur = db.execute("SELECT * FROM ENROLLMENTS WHERE student_id = ? AND section_id = ?", (student_id, course["id"]),)

        enrollment_student = enroll_cur.fetchone()

        if enrollment_student:
            db.execute("DELETE FROM ENROLLMENTS WHERE student_id = ?", (student_id,))
            db.commit()
            return {"message": "Student dropped from the course enrollment."}
        
        waitlist_cur = db.execute("SELECT * FROM WAITLIST WHERE student_id = ? AND section_id = ?", (student_id, course["id"]),)

        waitlist_student = waitlist_cur.fetchone()

        if waitlist_student:
            db.execute("DELETE FROM WAITLIST WHERE student_id = ? ", (student_id,))
            db.commit()
            return {"message": "Student dropped from the waitlist."}
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Student not found in any course section"
    )