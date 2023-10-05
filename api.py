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

class Course(BaseModel):
    department_code: str
    course_no: int
    title: str
    description: str

class Section(BaseModel):
    id: int = None
    dept_code: str = None
    course_num: int = None
    section_no: int = None
    semester: str = None
    year: int = None
    prof_id: int = None
    room_num: int = None
    room_capacity: int = None
    course_start_date: str = None
    enrollment_start: str = None
    enrollment_end: str = None

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

@app.post("/sections/", status_code=status.HTTP_201_CREATED)
def create_section(
    section: Section, response: Response, db: sqlite3.Connection = Depends(get_db)
):
    record = dict(section)
    try:
        cur = db.execute(
            """
            INSERT INTO course_section(id, dept_code, course_num, section_no, 
                    semester, year, prof_id, room_num, room_capacity, 
                    course_start_date, enrollment_start, enrollment_end)
            VALUES(:id, :dept_code, :course_num, :section_no,
                    :semester, :year, :prof_id, :room_num, :room_capacity, 
                    :course_start_date, :enrollment_start, :enrollment_end)
            """,
            record,
        )
        db.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    record["id"] = cur.lastrowid
    response.headers["Location"] = f"/sections/{record['id']}"
    return record

@app.delete("/sections/{id}", status_code=status.HTTP_200_OK)
def delete_section(id: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
    try:
        curr = db.execute("DELETE FROM course_section WHERE id=?;", [id])
        
        if curr.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Record not Found"
                )
        db.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )

    return {"message": "Record has been deleted successfully."}

@app.patch("/sections/{id}", status_code=status.HTTP_200_OK)
def update_section(id: int, section: Section, response: Response, db: sqlite3.Connection = Depends(get_db)):
    try:
        # Excluding fields that have not been set
        section = section.dict(exclude_unset=True)
        
        # Create a list of column-placeholder pairs, separated by commas
        keys = ", ".join([f"{key} = ?" for index, key in enumerate(section.keys())])
        
        # Create a list of values to bind to the placeholders
        values = list(section.values()) # List of values to be updated
        values.append(id) # WHERE id = ?

        # Define a parameterized query with placeholders & values
        update_query = f"UPDATE course_section SET {keys} WHERE id = ?"

        # Execute the query
        curr = db.execute(update_query, values)
        
        # Raise exeption if Record not Found
        if curr.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Record not Found"
                )
        db.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    return {"message": "Section updated successfully"}