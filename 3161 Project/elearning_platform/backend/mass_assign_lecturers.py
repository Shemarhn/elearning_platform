# mass_assign_lecturers.py

from enrollment_ops import assign_lecturer_to_course
import random
from db import create_connection, close_connection

def get_all_lecturers():
    """
    Retrieve all lecturer user IDs from the database.
    """
    connection = create_connection()
    if not connection:
        print("[-] Could not retrieve lecturers.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT id FROM users WHERE role = 'lecturer'"
        cursor.execute(sql)
        lecturers = cursor.fetchall()
        return [lecturer['id'] for lecturer in lecturers]

    except Exception as e:
        print(f"[-] Error retrieving lecturers: {e}")
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

def mass_assign_lecturers(min_courses=1, max_courses=5):
    """
    Assign lecturers to between 1 to 5 courses each, without exceeding 5 courses per lecturer.
    """
    lecturers = get_all_lecturers()
    courses = get_all_courses()

    if not lecturers or not courses:
        print("[-] No lecturers or courses available for assignment.")
        return

    # Shuffle courses to assign randomly
    random.shuffle(courses)
    lecturer_course_count = {lecturer_id: 0 for lecturer_id in lecturers}

    course_index = 0
    total_assigned = 0

    while course_index < len(courses):
        # Randomly pick a lecturer who has taught fewer than 5 courses
        available_lecturers = [lecturer for lecturer, count in lecturer_course_count.items() if count < max_courses]
        if not available_lecturers:
            print("[-] No available lecturers left who can take more courses.")
            break

        lecturer_id = random.choice(available_lecturers)
        course_id = courses[course_index]

        assign_lecturer_to_course(lecturer_id, course_id)
        lecturer_course_count[lecturer_id] += 1
        total_assigned += 1

        course_index += 1

        if total_assigned % 20 == 0:
            print(f"[+] Assigned lecturers to {total_assigned} courses...")

    print(f"[+] Completed assigning lecturers to {total_assigned} courses.")

if __name__ == "__main__":
    mass_assign_lecturers()
