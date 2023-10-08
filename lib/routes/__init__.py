from fastapi import APIRouter, Depends, Response, HTTPException, status

from lib.utils.enrollment_helper import enroll_students_from_waitlist, is_auto_enroll_enabled, get_opening_sections
from lib.models import Course, SectionCreate, SectionPatch, Student, Enrollment, Professor
from lib.db import get_db
import sqlite3
from datetime import datetime


router = APIRouter()


@router.post("/courses/", status_code=status.HTTP_201_CREATED)
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


@router.post("/sections/", status_code=status.HTTP_201_CREATED)
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


@router.delete("/sections/{id}", status_code=status.HTTP_200_OK)
def delete_section(
    id: int, response: Response, db: sqlite3.Connection = Depends(get_db)
):
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
                status_code=status.HTTP_404_NOT_FOUND, detail="Record not Found"
            )
        db.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )

    return {"message": "Item deleted successfully"}


@router.patch("/sections/{id}", status_code=status.HTTP_200_OK)
def update_section(
    id: int,
    section: SectionPatch,
    response: Response,
    db: sqlite3.Connection = Depends(get_db),
):
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
        section_fields = section.dict(exclude_unset=True)

        # Create a list of column-placeholder pairs, separated by commas
        keys = ", ".join(
            [f"{key} = ?" for index, key in enumerate(section_fields.keys())]
        )

        # Create a list of values to bind to the placeholders
        values = list(section_fields.values())  # List of values to be updated
        values.append(id)  # WHERE id = ?

        # Define a parameterized query with placeholders & values
        update_query = f"UPDATE course_section SET {keys} WHERE id = ?"

        # Execute the query
        curr = db.execute(update_query, values)

        # Raise exeption if Record not Found
        if curr.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Record not Found"
            )
        db.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    return {"message": "Section updated successfully"}


@router.get("/classes/")
def list_classes(db: sqlite3.Connection = Depends(get_db)):
    """
    List all available classes to the student

    Returns:
    - dict: A dictionary containing the details of the classes
    """

    classes = db.execute(
        "SELECT c.*, cs.id as section_id FROM course c inner join course_section cs  on c.department_code = cs.dept_code and c.course_no = cs.course_num"
    )
    return {"classes": classes.fetchall()}


from pydantic import BaseModel


@router.post("/enrollments/")
def enroll_students(enrollment: Enrollment, db: sqlite3.Connection = Depends(get_db)):
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
    response = ""
    max_enrollment_capacity = 30
    waitlist_capacity = 15

    course_dates = db.execute(
        "SELECT course_start_date, strftime('%Y-%m-%d',enrollment_start) as enrollment_start, strftime('%Y-%m-%d',enrollment_end) as enrollment_end FROM course_section where id = ?;",
        [enrollment.section_id],
    ).fetchone()

    if course_dates == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no sections found"
        )

    # course_start_date = datetime.strptime(course_dates['course_start_date'],'%Y-%m-%d')
    enrollment_start_date = datetime.strptime(
        course_dates["enrollment_start"], "%Y-%m-%d"
    )
    enrollment_end_date = datetime.strptime(course_dates["enrollment_end"], "%Y-%m-%d")

    ## enrollments not allowed pre and post enrollment dates as defined in the db
    # current_date = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    ## if current_date > course_start_date+timedelta(days=7) or current_date<enrollment_start_date:
    # if current_date > enrollment_end_date:
    #   # or current_date < enrollment_start_date
    #  raise HTTPException(
    #     status_code=400,
    #    detail="You are trying to enrolside the enrollment window",
    # )

    seats_taken = db.execute(
        "SELECT COUNT(*) FROM enrollments where section_id = ?;",
        [enrollment.section_id],
    ).fetchone()
    available_seats = max_enrollment_capacity - seats_taken[0]

    if available_seats > 0:
        # enrollment possible
        # check if student is already enrolled into section id > then return UNIQUE constraint key violation error
        already_enrolled = db.execute(
            "Select count(*) cnt from enrollments where section_id=? and student_id=?",
            (enrollment.section_id, enrollment.student_id),
        ).fetchone()
        if already_enrolled["cnt"] > 0:
            raise HTTPException(
                status_code=400, detail="Student already enrolled in this section"
            )

        db.execute(
            "INSERT INTO enrollments(section_id,student_id,enrollment_date) VALUES(?, ?, datetime('now'))",
            (enrollment.section_id, enrollment.student_id),
        )

        db.commit()
        response = f"Student {enrollment.student_id} enrolled successfully for section_id {enrollment.section_id}"

    elif available_seats == 0:
        # check waitlist capacity
        current_waitlist_capacity = db.execute(
            "SELECT COUNT(*) AS cnt FROM waitlist where section_id = ? group by section_id",
            (enrollment.section_id,),
        ).fetchone()

        print(current_waitlist_capacity[0])

        current_student_waitlist = db.execute(
            "SELECT COUNT(*) AS cnt FROM waitlist where section_id = ? and student_id = ?",
            (enrollment.section_id, enrollment.student_id),
        ).fetchone()

        print(current_student_waitlist)

        current_waitlist_capacity = current_waitlist_capacity["cnt"]
        current_student_waitlist = current_student_waitlist["cnt"]

        if (
            current_waitlist_capacity < waitlist_capacity
            and current_student_waitlist < 3
        ):
            # push student in waitlist table
            db.execute(
                "INSERT INTO waitlist(section_id,student_id,waitlist_date) VALUES(?, ?, datetime('now'))",
                (enrollment.section_id, enrollment.student_id),
            )
            db.commit()
            response = f"Student {enrollment.student_id} waitlisted successfully for {enrollment.section_id}"
    else:
        # enrollment not possible
        raise HTTPException(
            status_code=400,
            detail="Class capacity and waitlist is full, cannot enroll currently",
        )

    return {"enrollments": response}


@router.post("/freezeenrollment/{flag}")
def freeze_auto_enrollment(flag, db: sqlite3.Connection = Depends(get_db)):
    # toggle the flag
    flag = 0 if flag == 1 else 1

    db.execute("UPDATE configs set automatic_enrollment = ?;", [flag])
    db.commit()

    if flag == 1:
      opening_sections = get_opening_sections(db)
      enroll_students_from_waitlist(db, opening_sections)

    return {"status_code ": 200}

# Getting specific professors by using their id, then finding the courses they 
# teach to then find their current enrollments.

@router.get("/professors/{id}/enrollments")
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

@router.get("/professors/{id}/droplists")
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

@router.delete("/professors/{prof_id}/course_section/{section_id}/student/{student_id}/drop")
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

# get waitlist position for a student

@router.get("/student/waitlist/{section_id}/{student_id}")
def get_waitlist_position(
        section_id: int, student_id: int , db: sqlite3.Connection = Depends(get_db)
):
    position = -1

    try:
        waitlist = db.execute(
            "SELECT student_id as sid FROM waitlist WHERE section_id = ? ORDER BY waitlist_date ASC",
            [section_id]
        )

        for idx, item in enumerate(waitlist.fetchall()):
            print(idx, item["sid"])
            if student_id == item["sid"]:
                position = idx + 1

    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )

    return {"position": position}

# drop self from waitlist

@router.delete("/student/waitlist/{section_id}")
def delete_waitlist(
    section_id: int, student: Student, db: sqlite3.Connection = Depends(get_db)
):
    try:
        result = db.execute(
            "DELETE FROM waitlist WHERE section_id = ? AND student_id = ?;",
            [section_id, student.id],
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not delete because no such enrollments exist",
            )

        db.commit()

    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )

    return {"message": "successfully removed from waitlist"}

# list students in waitlist for a section/class

@router.get("/professor/waitlist/{section_id}")
def get_waitlist(section_id: int, db: sqlite3.Connection = Depends(get_db)):
    watilist = []

    try:
        results = db.execute(
            "SELECT * FROM waitlist WHERE section_id = ? ORDER BY waitlist_date ASC",
            [section_id]
        )

        if results.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="could not find the waitlist for that section",
            )

        waitlist = [r["student_id"] for r in results]

    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )

    return {"waitlist": waitlist}
