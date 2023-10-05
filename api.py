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

# class Student(BaseModel):
#     id: int
#     first_name: str
#     last_name: str
#     email: str

def get_db():
    with contextlib.closing(sqlite3.connect("./var/titanonline.db")) as db:
        db.row_factory = sqlite3.Row
        yield db

def get_logger():
    return logging.getLogger(__name__)

# settings = Settings()
app = FastAPI()


# logging.config.fileConfig(settings.logging_config, disable_existing_loggers=False)

# Testing API
# @app.get("/professors/")
# def get_professors(db: sqlite3.Connection = Depends(get_db)):
#     profesors = db.execute(f"SELECT * FROM PROFESSORS;")
#     return {"professors": profesors.fetchall()}


# Getting specific professors by using their id, then finding the courses they 
# teach to then find their current enrollments.
@app.get("/professors/{id}/course_sections")
def get_professor(
    id: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(f"SELECT * FROM PROFESSORS WHERE id = {id} LIMIT 1")
    professor = cur.fetchall()

    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found"
        )
    
    cur = db.execute(f"SELECT * FROM COURSE_SECTION WHERE prof_id = {id}")
    course_sections = cur.fetchall()

    course_sections_li = []

    for course in course_sections:
        course_sections_li.append(course)

    
    enrollment_li = []
    for course in course_sections_li:
        cur = db.execute(f"SELECT * FROM ENROLLMENTS WHERE section_id = {course['id']}")
        enrollments = cur.fetchall()
        
        enrollment_li.extend(enrollments)

    return {"professor": professor, "enrollments": enrollment_li}
