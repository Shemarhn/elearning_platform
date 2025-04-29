# generate_calendar_events.py

from db import create_connection, close_connection
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

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

def create_calendar_event(course_id, event_date, title, description):
    """
    Insert a calendar event for a given course.
    """
    connection = create_connection()
    if not connection:
        print("[-] Failed to create calendar event: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO calendar_events (course_id, event_date, title, description) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (course_id, event_date, title, description))
        connection.commit()
        return True

    except Exception as e:
        print(f"[-] Error during calendar event creation: {e}")
        return False

    finally:
        cursor.close()
        close_connection(connection)

def generate_calendar_events(min_events=5, max_events=10):
    """
    Generate a number of random calendar events for each course.
    """
    courses = get_all_courses()
    if not courses:
        print("[-] No courses available.")
        return

    event_types = ["Lecture", "Assignment Due", "Quiz", "Midterm Exam", "Final Exam", "Workshop", "Project Presentation"]

    total_created = 0

    for course_id in courses:
        num_events = random.randint(min_events, max_events)
        start_date = datetime.today()

        for _ in range(num_events):
            days_ahead = random.randint(1, 120)  # Random event within next 4 months
            event_date = start_date + timedelta(days=days_ahead)
            event_type = random.choice(event_types)
            title = f"{event_type} for Course {course_id}"
            description = fake.sentence(nb_words=10)

            create_calendar_event(course_id, event_date.date(), title, description)
            total_created += 1

        if course_id % 20 == 0:
            print(f"[+] Generated events for {course_id} courses...")

    print(f"[+] Completed generating {total_created} calendar events.")

if __name__ == "__main__":
    generate_calendar_events()
