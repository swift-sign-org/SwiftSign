from flask import blueprints, jsonify, session, request
from datetime import datetime
import base64
# from ..AI_Integration.face_recognition_asyn import get_face_vector

from BackEnd.Database.ProjectDatabase import Teacher, Class, Subject, Student ,db

api_bp = blueprints.Blueprint('api', __name__)

# In-memory attendance session state (replace with DB in production)
attendance_session = {
    'active': False,
    'students': [],  # List of dicts: {id, name, selfRecorded, status}
    'module': None,
    'group': None,
    'start_time': None
}

# Teacher login (POST /api/teachers/login)
@api_bp.route('/api/teachers/login', methods=['POST'])
def teacher_login():
    try:
        teacher_email = request.json['email']
        teacher_password = request.json['password']
        teacher = Teacher.query.filter_by(TeacherEmail=teacher_email).first()
        if not teacher:
            return jsonify({"message": "Invalid credentials: Invalid email"}), 401

        if not teacher.check_password(teacher_password):
            return jsonify({"message": "Invalid credentials: Invalid password"}), 401
        
        subjects = Subject.query.filter_by(TeacherIDInSubject=teacher.TeacherID).all()
        session['teacher_id'] = teacher.TeacherID
        return jsonify({"message": "Teacher login successful", "subjects": [subject.SubjectName for subject in subjects]}) , 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred during login"}), 500

# Student login (POST /api/students/login)
@api_bp.route('/api/students/login', methods=['POST'])
def student_login():
    try:
        student_email = request.json['email']
        student = Student.query.filter_by(StudentEmail=student_email).first()
        if not student:
            return jsonify({"message": "Invalid credentials: Invalid email"}), 401

        session['student_id'] = student.StudentID
        session['student_photo'] = student.StudentPhoto
        return jsonify({"message": "Student login successful"}),200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred during login"}), 500

# Student registration (POST /api/students)
@api_bp.route('/api/students', methods=['POST'])
def student_register():
    try:
        data = request.get_json()
        name = data.get('name')
        class_name = data.get('class')
        email = data.get('email')
        if not name or not class_name or not email:
            return jsonify({'message': 'All fields are required.'}), 400
        if Student.query.filter_by(StudentEmail=email).first():
            return jsonify({'message': 'Student already registered with this email.'}), 409
        new_student = Student(StudentName=name, StudentClass=class_name, StudentEmail=email)
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Registration successful! Please take your photo.'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred during registration.'}), 500

# Student photo registration (POST /api/students/<int:student_id>/photo)
@api_bp.route('/api/students/<int:student_id>/photo', methods=['POST'])
def student_register_photo(student_id):
    try:
        data = request.get_json()
        photo = data.get('photo')
        if not photo:
            return jsonify({'message': 'Photo is required.'}), 400
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'message': 'Student not found.'}), 404
        student.set_face_vector(base64.b64decode(photo))
        db.session.commit()
        return jsonify({'message': 'Photo saved successfully!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred while saving the photo.'}), 500

# Start attendance session (POST /api/attendance-sessions)
@api_bp.route('/api/attendance-sessions', methods=['POST'])
def start_attendance():
    if 'teacher_id' not in session:
        return jsonify({'message': 'Not authorized'}), 401
    data = request.get_json()
    module = data.get('module')
    group = data.get('group')
    if not module or not group:
        return jsonify({'message': 'Module and group required'}), 400
# Fetch students for this group/module (simplified)
    students = Student.query.all()  # TODO: filter by group/module
    attendance_session['active'] = True
    attendance_session['students'] = [
        {'id': s.StudentID, 'name': s.StudentName, 'selfRecorded': False, 'status': None}
        for s in students
    ]
    attendance_session['module'] = module
    attendance_session['group'] = group
    attendance_session['start_time'] = datetime.now().isoformat()
    return jsonify({'message': 'Attendance session started'}), 200

# End current attendance session (POST /api/attendance-sessions/current/end)
@api_bp.route('/api/attendance-sessions/current/end', methods=['POST'])
def end_attendance():
    if 'teacher_id' not in session:
        return jsonify({'message': 'Not authorized'}), 401
    attendance_session['active'] = False
    return jsonify({'message': 'Attendance session ended'}), 200

# Get students in current attendance session (GET /api/attendance-sessions/current/students)
@api_bp.route('/api/attendance-sessions/current/students', methods=['GET'])
def attendance_students():
    if not attendance_session['active']:
        return jsonify({'students': []}), 200
    return jsonify({'students': attendance_session['students']}), 200

# Mark student attendance (PATCH /api/attendance-sessions/current/students/<int:student_id>)
@api_bp.route('/api/attendance-sessions/current/students/<int:student_id>', methods=['PATCH'])
def mark_attendance(student_id):
    if 'teacher_id' not in session:
        return jsonify({'message': 'Not authorized'}), 401
    data = request.get_json()
    status = data.get('status')
    for s in attendance_session['students']:
        if s['id'] == student_id:
            s['status'] = status
            break
    return jsonify({'message': f'Student marked as {status}'}), 200

# Student self-attendance (POST /api/attendance-records)
@api_bp.route('/api/attendance-records', methods=['POST'])
def attendanceRecord():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
        student_photo = data.get('photo')
        if not student_photo:
            return jsonify({"message": "Invalid photo: photo not found"}), 400
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({"message": "Not authorized: please log in again"}), 401
        stored_face_vector = session.get('face_vector')
        if not stored_face_vector:
            return jsonify({"message": "Student photo not found in session"}), 404
        for s in attendance_session['students']:
            if s['id'] == student_id:
                s['selfRecorded'] = True
                s['status'] = 'present'
                break
        return jsonify({"message": "Attendance recorded successfully"}), 200
    except KeyError as e:
        print(f"Missing key in request: {e}")
        return jsonify({"message": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        print(f"Error recording attendance: {e}")
        return jsonify({"message": "An error occurred while recording attendance"}), 500

# Get attendance records (GET /api/attendance-records)
@api_bp.route('/api/attendance-records', methods=['GET'])
def get_attendanceRecord():
    try:
        teacher_id = session.get('teacher_id')
        if not teacher_id:
            return jsonify({"message": "Teacher not logged in"}), 401
        attendance_records = []
        return jsonify({"attendance_records": attendance_records}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while fetching attendance records"}), 500
