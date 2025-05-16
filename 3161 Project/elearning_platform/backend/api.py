# elearning_api.py (Refactored with SQLAlchemy + PyMySQL)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import text
from flask_cors import CORS
import pymysql

import pymysql
from functools import wraps
pymysql.install_as_MySQLdb()

app = Flask(__name__)
CORS(app)

# === CONFIG ===
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pass1@localhost/elearning_platform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# === HELPERS ===
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            current_user = get_jwt_identity()
            result = db.session.execute("SELECT role FROM users WHERE userid = %s", (current_user,)).fetchone()
            if result and result[0] == role:
                return fn(*args, **kwargs)
            return jsonify({'message': 'Access forbidden'}), 403
        return decorated
    return wrapper


# === AUTH ===
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    userid = data['userid']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    role = data['role']
    db.session.execute(
    text("INSERT INTO users (userid, password_hash, role) VALUES (:userid, :password, :role)"),
    {"userid": userid, "password": password, "role": role})
    return jsonify({'message': 'User registered successfully'})

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    userid = data['userid']
    password = data['password']
    result = db.session.execute("SELECT password_hash FROM users WHERE userid = %s", (userid,)).fetchone()
    if result and bcrypt.check_password_hash(result[0], password):
        token = create_access_token(identity=userid)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# === COURSES ===
@app.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    result = db.session.execute("SELECT * FROM courses")
    return jsonify([dict(row) for row in result])

@app.route('/courses/create', methods=['POST'])
@role_required('admin')
def create_course():
    data = request.get_json()
    db.session.execute("INSERT INTO courses (title, description) VALUES (%s, %s)", (data['title'], data['description']))
    db.session.commit()
    return jsonify({'message': 'Course created'})

@app.route('/courses/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_courses(student_id):
    result = db.session.execute("""
        SELECT c.* FROM courses c
        JOIN course_registrations cr ON c.id = cr.course_id
        WHERE cr.student_id = %s
    """, (student_id,))
    return jsonify([dict(row) for row in result])

@app.route('/courses/lecturer/<int:lecturer_id>', methods=['GET'])
@jwt_required()
def get_lecturer_courses(lecturer_id):
    result = db.session.execute("""
        SELECT c.* FROM courses c
        JOIN course_lecturers cl ON c.id = cl.course_id
        WHERE cl.lecturer_id = %s
    """, (lecturer_id,))
    return jsonify([dict(row) for row in result])

# === REGISTRATION ===
@app.route('/courses/enroll', methods=['POST'])
@role_required('student')
def enroll_course():
    data = request.get_json()
    db.session.execute("INSERT INTO course_registrations (student_id, course_id) VALUES (%s, %s)", (data['student_id'], data['course_id']))
    db.session.commit()
    return jsonify({'message': 'Enrolled in course'})

@app.route('/courses/<int:course_id>/members', methods=['GET'])
@jwt_required()
def get_course_members(course_id):
    result = db.session.execute("SELECT u.id, u.userid FROM users u JOIN course_registrations cr ON u.id = cr.student_id WHERE cr.course_id = %s", (course_id,))
    return jsonify([dict(row) for row in result])

# === EVENTS ===
@app.route('/calendar/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course_events(course_id):
    result = db.session.execute("SELECT * FROM calendar_events WHERE course_id = %s", (course_id,))
    return jsonify([dict(row) for row in result])

@app.route('/calendar/create', methods=['POST'])
@jwt_required()
def create_event():
    data = request.get_json()
    db.session.execute("""
        INSERT INTO calendar_events (course_id, event_date, title, description)
        VALUES (%s, %s, %s, %s)
    """, (data['course_id'], data['event_date'], data['title'], data['description']))
    db.session.commit()
    return jsonify({'message': 'Event created'})

# === FORUMS ===
@app.route('/forums/<int:course_id>', methods=['GET'])
@jwt_required()
def get_forums(course_id):
    result = db.session.execute("SELECT * FROM forums WHERE course_id = %s", (course_id,))
    return jsonify([dict(row) for row in result])

@app.route('/forums/create', methods=['POST'])
@jwt_required()
def create_forum():
    data = request.get_json()
    db.session.execute("INSERT INTO forums (course_id, title) VALUES (%s, %s)", (data['course_id'], data['title']))
    db.session.commit()
    return jsonify({'message': 'Forum created'})

# === THREADS ===
@app.route('/threads/<int:forum_id>', methods=['GET'])
@jwt_required()
def get_threads(forum_id):
    result = db.session.execute("SELECT * FROM discussion_threads WHERE forum_id = %s", (forum_id,))
    return jsonify([dict(row) for row in result])

@app.route('/threads/create', methods=['POST'])
@jwt_required()
def create_thread():
    data = request.get_json()
    user_id = get_jwt_identity()
    db.session.execute("""
        INSERT INTO discussion_threads (forum_id, title, content, user_id)
        VALUES (%s, %s, %s, (SELECT id FROM users WHERE userid = %s))
    """, (data['forum_id'], data['title'], data['content'], user_id))
    db.session.commit()
    return jsonify({'message': 'Thread created'})

# === REPLIES ===
@app.route('/replies/create', methods=['POST'])
@jwt_required()
def create_reply():
    data = request.get_json()
    user_id = get_jwt_identity()
    db.session.execute("""
        INSERT INTO replies (thread_id, parent_reply_id, content, user_id)
        VALUES (%s, %s, %s, (SELECT id FROM users WHERE userid = %s))
    """, (data['thread_id'], data.get('parent_reply_id'), data['content'], user_id))
    db.session.commit()
    return jsonify({'message': 'Reply created'})

# === ASSIGNMENTS ===
@app.route('/assignments/submit', methods=['POST'])
@role_required('student')
def submit_assignment():
    data = request.get_json()
    db.session.execute("""
        INSERT INTO assignments (course_id, student_id, title, file_link, grade)
        VALUES (%s, %s, %s, %s, NULL)
    """, (data['course_id'], data['student_id'], data['title'], data['file_link']))
    db.session.commit()
    return jsonify({'message': 'Assignment submitted'})

@app.route('/assignments/grade', methods=['POST'])
@role_required('lecturer')
def grade_assignment():
    data = request.get_json()
    db.session.execute("""
        UPDATE assignments SET grade = %s WHERE course_id = %s AND student_id = %s AND title = %s
    """, (data['grade'], data['course_id'], data['student_id'], data['title']))
    db.session.commit()
    return jsonify({'message': 'Grade submitted'})

# === REPORTS ===
@app.route('/reports/courses_50_plus', methods=['GET'])
def report_courses_50_plus():
    result = db.session.execute("""
        SELECT course_id, COUNT(student_id) as student_count FROM course_registrations
        GROUP BY course_id HAVING student_count >= 50
    """)
    return jsonify([dict(row) for row in result])

@app.route('/reports/students_5_plus', methods=['GET'])
def report_students_5_plus():
    result = db.session.execute("""
        SELECT student_id, COUNT(course_id) as course_count FROM course_registrations
        GROUP BY student_id HAVING course_count >= 5
    """)
    return jsonify([dict(row) for row in result])

@app.route('/reports/lecturers_3_plus', methods=['GET'])
def report_lecturers_3_plus():
    result = db.session.execute("""
        SELECT lecturer_id, COUNT(course_id) as course_count FROM course_lecturers
        GROUP BY lecturer_id HAVING course_count >= 3
    """)
    return jsonify([dict(row) for row in result])

@app.route('/reports/top_courses', methods=['GET'])
def report_top_courses():
    result = db.session.execute("""
        SELECT course_id, COUNT(student_id) as enrollment_count FROM course_registrations
        GROUP BY course_id ORDER BY enrollment_count DESC LIMIT 10
    """)
    return jsonify([dict(row) for row in result])

@app.route('/reports/top_students', methods=['GET'])
def report_top_students():
    result = db.session.execute("""
        SELECT student_id, AVG(grade) as average_grade FROM assignments
        WHERE grade IS NOT NULL GROUP BY student_id ORDER BY average_grade DESC LIMIT 10
    """)
    return jsonify([dict(row) for row in result])

if __name__ == '__main__':
    app.run(debug=True)
