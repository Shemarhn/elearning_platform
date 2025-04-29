# enrollment_ops.py

from db import create_connection, close_connection

def enroll_student_in_course(student_id, course_id):
    """
    Enroll a student into a course.
    """
    connection = create_connection()
    if not connection:
        print("[-] Enrollment failed: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO course_registrations (student_id, course_id) VALUES (%s, %s)"
        cursor.execute(sql, (student_id, course_id))
        connection.commit()
        print(f"[+] Student ID {student_id} enrolled in Course ID {course_id}.")
        return True

    except Exception as e:
        print(f"[-] Error during enrollment: {e}")
        return False

    finally:
        cursor.close()
        close_connection(connection)

def assign_lecturer_to_course(lecturer_id, course_id):
    """
    Assign a lecturer to teach a course.
    """
    connection = create_connection()
    if not connection:
        print("[-] Lecturer assignment failed: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO course_lecturers (lecturer_id, course_id) VALUES (%s, %s)"
        cursor.execute(sql, (lecturer_id, course_id))
        connection.commit()
        print(f"[+] Lecturer ID {lecturer_id} assigned to Course ID {course_id}.")
        return True

    except Exception as e:
        print(f"[-] Error during lecturer assignment: {e}")
        return False

    finally:
        cursor.close()
        close_connection(connection)
