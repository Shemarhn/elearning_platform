# course_ops.py

from db import create_connection, close_connection

def create_course(title, description):
    """
    Admin-only function to create a new course.
    """
    connection = create_connection()
    if not connection:
        print("[-] Failed to create course: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO courses (title, description) VALUES (%s, %s)"
        cursor.execute(sql, (title, description))
        connection.commit()
        print(f"[+] Course '{title}' created successfully.")
        return True

    except Exception as e:
        print(f"[-] Error during course creation: {e}")
        return False

    finally:
        cursor.close()
        close_connection(connection)

def get_all_courses():
    """
    Retrieve all available courses.
    """
    connection = create_connection()
    if not connection:
        print("[-] Failed to retrieve courses: No DB connection.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT * FROM courses"
        cursor.execute(sql)
        courses = cursor.fetchall()
        print(f"[+] Retrieved {len(courses)} courses.")
        return courses

    except Exception as e:
        print(f"[-] Error retrieving courses: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)

def get_courses_for_student(student_id):
    """
    Retrieve courses registered by a specific student.
    """
    connection = create_connection()
    if not connection:
        print("[-] Failed to retrieve student courses: No DB connection.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = """
        SELECT c.*
        FROM courses c
        JOIN course_registrations cr ON c.id = cr.course_id
        WHERE cr.student_id = %s
        """
        cursor.execute(sql, (student_id,))
        courses = cursor.fetchall()
        print(f"[+] Retrieved {len(courses)} courses for student ID {student_id}.")
        return courses

    except Exception as e:
        print(f"[-] Error retrieving courses for student: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)

def get_courses_for_lecturer(lecturer_id):
    """
    Retrieve courses taught by a specific lecturer.
    """
    connection = create_connection()
    if not connection:
        print("[-] Failed to retrieve lecturer courses: No DB connection.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = """
        SELECT c.*
        FROM courses c
        JOIN course_lecturers cl ON c.id = cl.course_id
        WHERE cl.lecturer_id = %s
        """
        cursor.execute(sql, (lecturer_id,))
        courses = cursor.fetchall()
        print(f"[+] Retrieved {len(courses)} courses for lecturer ID {lecturer_id}.")
        return courses

    except Exception as e:
        print(f"[-] Error retrieving courses for lecturer: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)
