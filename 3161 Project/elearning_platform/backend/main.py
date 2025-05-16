# main.py

from flask import Flask
from user_ops import register_user, login_user
from course_ops import create_course, get_all_courses
from enrollment_ops import enroll_student_in_course, assign_lecturer_to_course
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # replace with your frontend URL and port


# --- Test User Registration ---
register_user('test_admin', 'Password123!', 'admin')

# --- Test User Login ---
user = login_user('test_admin', 'Password123!')
if user:
    print("[TEST] Logged in User:", user)

# --- Test Course Creation (Admin Only) ---
create_course('Introduction to Cybersecurity', 'Basics of cybersecurity, threats, and prevention.')

# --- Test Retrieve All Courses ---
courses = get_all_courses()
for course in courses:
    print(f"[TEST] Course: {course['title']} - {course['description']}")


# Test enroll a student manually
enroll_student_in_course(student_id=1, course_id=1)

# Test assign a lecturer manually
assign_lecturer_to_course(lecturer_id=2, course_id=1)