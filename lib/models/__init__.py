from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings

# import logging.config


class Settings(BaseSettings, env_file="../.env", extra="ignore"):
    database: str
    # logging_config: str


class Student(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


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
    dept_code: str
    course_num: int
    section_no: int
    semester: str
    year: int
    prof_id: int
    room_num: int
    course_start_date: str
    enrollment_start: str
    enrollment_end: str


class Enrollment(BaseModel):
    student_id: int
    section_id: int
