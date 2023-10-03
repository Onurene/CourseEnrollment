from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import List
import sqlite3


class Course(BaseModel):
    department_code: str
    course_no: int
    title: str
    description: str

@asynccontextmanager
async def db_conn():
    conn = sqlite3.connect()
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        await conn.close()


app = FastAPI()


@app.get("/courses")
def get_courses() -> List[Course]:
    async with db_conn() as db:
    conn = sqlite3.connect('./var/titanonline.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * FROM course;').fetchall()
    courses = [dict(ix) for ix in rows]
    return courses

