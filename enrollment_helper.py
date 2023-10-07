import sqlite3
from typing import Optional
from fastapi import HTTPException, status

def is_auto_enroll_enabled(db: sqlite3.Connection):
    """
    Check if automatic enrollment is enabled

    Parameters:
        db (sqlite3.Connection): Database connection.

    Returns:
        bool: True if automatic enrollment is enabled. Otherwise, False.
    """
    return True

def get_opening_sections(db: sqlite3.Connection):
    """
    Get sections which have available seats

    Parameters:
        db (sqlite3.Connection): Database connection.

    Returns:
        list[int]: A list of section_id.
    """

    cursor = db.execute(
        """
        SELECT id 
        FROM course_section 
        WHERE DATE('now') <= date(course_start_date, '+14 days') AND
            room_capacity > (SELECT COUNT(student_id)
                            FROM enrollments
                            WHERE section_id = id
                            )
        """)
    rows = cursor.fetchall()
    return [row[0] for row in rows]

def auto_enroll(db: sqlite3.Connection, section_id_list: Optional[list[int]] = None):
    """
    This function checks the waitlist for available spots in the sections
    and enrolls students accordingly.

    Parameters:
        db (sqlite3.Connection): Database connection.

    Returns:
        int: The number of success enrollments.
    """
    
    enrollment_count = 0

    try:
        for e in section_id_list:
            cursor = db.execute(
            """
            INSERT INTO enrollments (section_id, student_id, enrollment_date)
                SELECT section_id, student_id, datetime('now')
                FROM waitlist
                WHERE section_id=$0
                ORDER BY waitlist_date ASC
                LIMIT (
                        (SELECT room_capacity 
                        FROM course_section
                        WHERE id=$0) - (SELECT COUNT(student_id)
                                        FROM enrollments
                                        WHERE section_id=$0
                                        )
                    );
            """, [e])

            cursor = db.execute(
            """
            DELETE FROM waitlist
            WHERE student_id IN (
                SELECT student_id
                FROM waitlist
                ORDER BY waitlist_date
                LIMIT $0
            );
            """, [cursor.rowcount])

            enrollment_count += cursor.rowcount
        
        db.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    return enrollment_count