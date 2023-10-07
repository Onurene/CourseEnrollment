import contextlib
import logging.config
import sqlite3
from typing import Optional

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

@app.post("/courses/", status_code=status.HTTP_201_CREATED)
def create_course(
    course: Course, response: Response, db: sqlite3.Connection = Depends(get_db)
):
    """
    Create course
    
    Creates a new course with the provided details.
    
    Parameters:
    - `course` (CourseInput): JSON body input for the course with the following fields:
        - `department_code` (str): The department code for the course.
        - `course_no` (int): The course number.
        - `title` (str): The title of the course.
        - `description` (str): A description of the course.

    Returns:
    - dict: A dictionary containing the details of the created item.
    
    Raises:
    - HTTPException (409): If a conflict occurs (e.g., duplicate course).
    """
    record = dict(course)
    try:
        cur = db.execute(
            """
            INSERT INTO course(department_code, course_no, title, description)
            VALUES(:department_code, :course_no, :title, :description)
            """,
            record,
        )
        db.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    return record

