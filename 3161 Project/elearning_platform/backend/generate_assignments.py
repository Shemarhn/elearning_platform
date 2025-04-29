# generate_assignments.py

from db import create_connection, close_connection
import random
from faker import Faker

fake = Faker()

ASSIGNMENT_TITLES = [
    "Research Paper on AI Ethics",
    "Physics Lab Report 2",
    "Essay on Renaissance Art",
    "Financial Accounting Case Study",
    "Database Design Project",
    "Software Engineering Midterm Project",
    "Marketing Strategy Proposal",
    "Sociology of Education Final Essay",
    "Environmental Science Data Analysis",
    "Web Development Portfolio",
    "Mobile App Wireframe Design",
    "Statistical Analysis Report",
    "Public Speaking Presentation",
    "Creative Writing Short Story",
    "Political Science Debate Paper",
    "Health and Wellness Plan",
    "Business Law Contract Draft",
    "Philosophy Reflection Essay",
    "Astronomy Observational Log",
    "Entrepreneurship Business Model Canvas"
]

def get_all_students():
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

def get_student_courses(student_id):
    connection = create_connection()
    if not connection:
        print("[-] Could not retrieve student courses.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT course_id FROM course_registrations WHERE student_id = %s"
        cursor.execute(sql, (student_id,))
        courses = cursor.fetchall()
        return [course['course_id'] for course in courses]

    except Exception as e:
        print(f"[-] Error retrieving courses for student: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)

def submit_assignment(course_id, student_id, title, file_link, grade):
    connection = create_connection()
    if not connection:
        print("[-] Failed to submit assignment: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO assignments (course_id, student_id, title, file_link, grade) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (course_id, student_id, title, file_link, grade))
        connection.commit()
        return True

    except Exception as e:
        print(f"[-] Error during assignment submission: {e}")
        return False

    finally:
        cursor.close()
        close_connection(connection)

def generate_assignments(min_assignments=1, max_assignments=3):
    students = get_all_students()

    if not students:
        print("[-] No students found.")
        return

    total_submissions = 0

    for student_id in students:
        student_courses = get_student_courses(student_id)
        if not student_courses:
            continue

        num_assignments = random.randint(min_assignments, max_assignments)
        selected_courses = random.sample(student_courses, min(num_assignments, len(student_courses)))

        for course_id in selected_courses:
            title = random.choice(ASSIGNMENT_TITLES)
            file_link = fake.url()
            grade = round(random.uniform(50, 100), 2)  # Grades between 50% and 100%
            submit_assignment(course_id, student_id, title, file_link, grade)
            total_submissions += 1

        if student_id % 1000 == 0:
            print(f"[+] Submitted assignments for {student_id} students...")

    print(f"[+] Completed {total_submissions} assignment submissions.")

if __name__ == "__main__":
    generate_assignments()
