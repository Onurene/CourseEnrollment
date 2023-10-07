import contextlib
import logging.config
import sqlite3
from typing import Optional
import collections
from datetime import timedelta, datetime

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

@app.post("/sections/", status_code=status.HTTP_201_CREATED)
def create_section(
    section: SectionCreate, response: Response, db: sqlite3.Connection = Depends(get_db)
):
    """
    Create Section
    
    Creates a new section.
    
    Parameters:
    - `section` (Section): The JSON object representing the section with the following properties:
        - `id` (int): The section ID.
        - `dept_code` (str): Department code.
        - `course_num` (int): Course number.
        - `section_no` (int): Section number.
        - `semester` (str): Semester name (SP, SU, FA, WI).
        - `year` (int): Academic year.
        - `prof_id` (int): Professor ID.
        - `room_num` (int): Room number.
        - `room_capacity` (int): Room capacity.
        - `course_start_date` (str): Course start date (format: "YYYY-MM-DD").
        - `enrollment_start` (str): Enrollment start date (format: "YYYY-MM-DD HH:MM:SS.SSS").
        - `enrollment_end` (str): Enrollment end date (format: "YYYY-MM-DD HH:MM:SS.SSS").
        
    Returns:
    - dict: A dictionary containing the details of the created item.
    
    Raises:
    - HTTPException (409): If a conflict occurs (e.g., duplicate course).
    """
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
    """
    Delete section
    
    Deletes a specific section.
    
    Parameters:
    - `id` (int): The ID of the section to delete.
    
    Returns:
    - dict: A dictionary indicating the success of the deletion operation.
      Example: {"message": "Item deleted successfully"}
    
    Raises:
    - HTTPException (404): If the section with the specified ID is not found.
    - HTTPException (409): If there is a conflict in the delete operation.
    """
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

    return {"message": "Item deleted successfully"}

@app.patch("/sections/{id}", status_code=status.HTTP_200_OK)
def update_section(id: int, section: SectionPatch, response: Response, db: sqlite3.Connection = Depends(get_db)):
    """
    Patch Section
    
    Updates specific details of a section.
    
    Parameters:
    - `section` (Section): The JSON object representing the section with the following properties:
        - `section_no` (int, optional): Section number.
        - `prof_id` (int, optional): Professor ID.
        - `room_num` (int, optional): Room number.
        - `room_capacity` (int, optional): Room capacity.
        - `course_start_date` (str, optional): Course start date (format: "YYYY-MM-DD").
        - `enrollment_start` (str, optional): Enrollment start date (format: "YYYY-MM-DD HH:MM:SS.SSS").
        - `enrollment_end` (str, optional): Enrollment end date (format: "YYYY-MM-DD HH:MM:SS.SSS").
    
    Returns:
    - dict: A dictionary indicating the success of the update operation.
      Example: {"message": "Section updated successfully"}
      
    Raises:
    - HTTPException (404): If the section with the specified ID is not found.
    - HTTPException (409): If there is a conflict in the update operation (e.g., duplicate section details).
    """
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

@app.get("/classes/")
def list_classes(db: sqlite3.Connection = Depends(get_db)):
    """
    List all available classes to the student

    Returns:
    - dict: A dictionary containing the details of the classes
    """

    classes = db.execute("SELECT c.*, cs.section_no as section_no FROM course c inner join course_section cs  on c.department_code = cs.dept_code and c.course_no = cs.course_num")
    return {"classes": classes.fetchall()}

@app.post("/enrollments/{student_id}/{course_no}/{section_no}")
def enroll_students(student_id, course_no, section_no, db: sqlite3.Connection = Depends(get_db)):
    """
    Lets a student enroll into the class

    Returns either of the success messages based on the class room capacity and waitlist capacity
    - student successfully enrolled into the class
    - student successfully waitlisted into the class

    Raises:
    - HTTPException (400): If student tries to enroll outside the enrollment window).
    - HTTPException (400): If student has already enrolled into the class.
    - HTTPException (400): Class and waitlist capacity is full, cannot enroll

    """
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

    elif class_capacity==0:
        # check waitlist capacity
        current_waitlist_capacity = db.execute("SELECT COUNT(*) cnt FROM waitlist where section_id = ? group by section_id",(section_id,)).fetchone()
        current_student_waitlist = db.execute("SELECT COUNT(*) cnt FROM waitlist where section_id = ? and student_id = ? group by section_id,student_id",(section_id,student_id)).fetchone()

        current_waitlist_capacity = current_waitlist_capacity['cnt']
        current_student_waitlist = current_student_waitlist['cnt']
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
    db.execute("UPDATE configs set automatic_enrollment = ?",(flag,))
    db.commit()
    return {"status_code ": 200}
