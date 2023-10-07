from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import contextmanager
from typing import List, Optional
import sqlite3


class Course(BaseModel):
    department_code: str
    course_no: int
    title: str
    description: str


@contextmanager
def db_conn():
    with sqlite3.connect('./var/titanonline.db') as conn:
        conn.row_factory = sqlite3.Row
        yield conn


app = FastAPI()


@app.get("/courses")
def get_courses() -> List[Course]:
    with db_conn() as db:
        rows = db.execute('SELECT * FROM course;').fetchall()
        courses = [dict(item) for item in rows]

    return courses


@app.get("/course/{dept}/{course_no}")
def get_course_sections(dept: str, course_no: int):
    with db_conn() as db:
        course = db.execute('SELECT * FROM course_section WHERE dept_code=? AND course_num=?', [ dept, course_no ]).fetchone()

        return course

