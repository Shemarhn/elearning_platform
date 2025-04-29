# mass_enroll_students.py

from enrollment_ops import enroll_student_in_course
import random
from db import create_connection, close_connection

def get_all_students():
    """
    Retrieve all student user IDs from the database.
    """
    connection = create_connection()
    if not connection:
        print("[-] Could not retrieve students.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT id FROM users WHERE role = 'student'"
        cursor.execute(sql)
        students = cursor.fetchall()
        return [student['id'] for student in students]

    except Exception as e:
        print(f"[-] Error retrieving students: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)

def get_all_courses():
    """
    Retrieve all course IDs from the database.
    """
    connection = create_connection()
    if not connection:
        print("[-] Could not retrieve courses.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT id FROM courses"
        cursor.execute(sql)
        courses = cursor.fetchall()
        return [course['id'] for course in courses]

    except Exception as e:
        print(f"[-] Error retrieving courses: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)

def mass_enroll_students(min_courses=3, max_courses=6):
    """
    Enroll each student in between 3 to 6 random courses.
    """
    students = get_all_students()
    courses = get_all_courses()

    if not students or not courses:
        print("[-] No students or courses available for enrollment.")
        return

    total_enrollments = 0

    for student_id in students:
        num_courses = random.randint(min_courses, max_courses)
        selected_courses = random.sample(courses, num_courses)

        for course_id in selected_courses:
            enroll_student_in_course(student_id, course_id)
            total_enrollments += 1

        if student_id % 1000 == 0:
            print(f"[+] Processed enrollments for {student_id} students...")

    print(f"[+] Completed mass enrollment. Total enrollments: {total_enrollments}")

if __name__ == "__main__":
    mass_enroll_students()
 