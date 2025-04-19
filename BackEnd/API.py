from flask import blueprints, jsonify, session, request
from datetime import datetime
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

@api_bp.route('/api/teacher_login', methods=['POST'])
def teacher_login():
    # Logic for teacher 
    try:
        teacher_email = request.json['email']
        teacher_password = request.json['password']
        # Here you would typically check the credentials against a database
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

@api_bp.route('/api/student_login', methods=['POST'])
def student_login():
    # Logic for student login
    try:
        student_email = request.json['email']
        student = Student.query.filter_by(StudentEmail=student_email).first()
        if not student:
            return jsonify({"message": "Invalid credentials: Invalid email"}), 401

        session['student_id'] = student.StudentID
        # just a mimik function untill ai is implemented
        session['student_photo'] = student.StudentPhoto
        return jsonify({"message": "Student login successful"}),200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred during login"}), 500

@api_bp.route('/api/student_register', methods=['POST'])
def student_register():
    try:
        data = request.get_json()
        name = data.get('name')
        class_name = data.get('class')
        email = data.get('email')
        if not name or not class_name or not email:
            return jsonify({'message': 'All fields are required.'}), 400
        # Check if student already exists
        if Student.query.filter_by(StudentEmail=email).first():
            return jsonify({'message': 'Student already registered with this email.'}), 409
        # Create new student (photo will be added later)
        new_student = Student(StudentName=name, StudentClass=class_name, StudentEmail=email)
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Registration successful! Please take your photo.'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred during registration.'}), 500

@api_bp.route('/api/student_register_photo', methods=['POST'])
def student_register_photo():
    try:
        data = request.get_json()
        email = data.get('email')
        photo = data.get('photo')
        if not email or not photo:
            return jsonify({'message': 'Email and photo are required.'}), 400
        student = Student.query.filter_by(StudentEmail=email).first()
        if not student:
            return jsonify({'message': 'Student not found.'}), 404
        student.StudentPhoto = photo
        db.session.commit()
        return jsonify({'message': 'Photo saved successfully!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred while saving the photo.'}), 500

@api_bp.route('/api/start_attendance', methods=['POST'])
def start_attendance():
    """
    Teacher starts an attendance session. Only one session at a time (per module/group).
    """
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

@api_bp.route('/api/end_attendance', methods=['POST'])
def end_attendance():
    """
    Teacher ends the attendance session.
    """
    if 'teacher_id' not in session:
        return jsonify({'message': 'Not authorized'}), 401
    attendance_session['active'] = False
    return jsonify({'message': 'Attendance session ended'}), 200

@api_bp.route('/api/attendance_students', methods=['GET'])
def attendance_students():
    """
    Returns the list of students and their attendance status for the current session.
    """
    if not attendance_session['active']:
        return jsonify({'students': []}), 200
    return jsonify({'students': attendance_session['students']}), 200

@api_bp.route('/api/mark_attendance', methods=['POST'])
def mark_attendance():
    """
    Teacher manually marks a student as present/absent.
    """
    if 'teacher_id' not in session:
        return jsonify({'message': 'Not authorized'}), 401
    data = request.get_json()
    student_id = data.get('student_id')
    status = data.get('status')
    for s in attendance_session['students']:
        if s['id'] == student_id:
            s['status'] = status
            break
    return jsonify({'message': 'Student marked as ' + status}), 200

@api_bp.route('/api/attendanceRecord', methods=['POST'])
def attendanceRecord():
    # Logic for attendance record
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        # Extract required fields
        student_photo = data.get('student_photo')
        attendance_status = data.get('attendance_status')
        
        # Validate input data
        if not student_photo:
            return jsonify({"message": "Invalid photo: photo not found"}), 400
        
        if not attendance_status:
            return jsonify({"message": "Invalid status: attendance status not provided"}), 400
        
        # Get student ID from session
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({"message": "Not authorized: please log in again"}), 401
        
        # Get the student's stored photo from session
        database_photo = session.get('student_photo')
        if not database_photo:
            return jsonify({"message": "Student photo not found in session"}), 404
        
        # In a real implementation, you would perform image comparison/facial recognition here
        # For now, we're simulating the check with a placeholder comparison
        # This would need to be replaced with actual ML-based facial recognition
        
        # If authentication is successful, record the attendance
        # Here you would add the record to your database
        # attendance_record = AttendanceRecord(
        #     StudentID=student_id,
        #     Date=datetime.now(),
        #     Status=attendance_status
        # )
        # with db.session.begin():
        #     db.session.add(attendance_record)
        #     db.session.commit()
        
        # After successful attendance, update session
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


@api_bp.route('/api/attendanceRecord', methods=['GET'])
def get_attendanceRecord():
    # here we send the teacher the file containing the attendance record
    # Logic for fetching attendance record
    try:
        teacher_id = session.get('teacher_id')
        if not teacher_id:
            return jsonify({"message": "Teacher not logged in"}), 401

        # Fetch attendance records from the database
        attendance_records = []  # Replace with actual database query to fetch records

        return jsonify({"attendance_records": attendance_records}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while fetching attendance records"}), 500
