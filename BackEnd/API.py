from flask import blueprints, jsonify, session, request
from datetime import datetime
import base64
import os
import tempfile
from AI_Integration.face_recognition_asyn import get_face_vector, compare_face_vectors

from BackEnd.Database.ProjectDatabase import Teacher, Class, Subject, Student, db

api_bp = blueprints.Blueprint('api', __name__)

# In-memory attendance session state (replace with DB in production)
attendance_session = {
    'active': False,
    'students': [],  # List of dicts: {id, name, email, selfRecorded, status}
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
        
        # Get subjects taught by this teacher
        subjects = Subject.query.filter_by(TeacherIDInSubject=teacher.TeacherID).all()
        session['teacher_id'] = teacher.TeacherID
        session['teacher_name'] = teacher.TeacherName
        
        return jsonify({
            "message": "Teacher login successful", 
            "subjects": [subject.SubjectName for subject in subjects]
        }), 200
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

        # Check if attendance is active
        if not attendance_session['active']:
            return jsonify({"message": "No active attendance session"}), 403
            
        # Check if student is in the active class/group
        is_in_session = False
        for s in attendance_session['students']:
            if s['email'] == student_email:
                is_in_session = True
                break
                
        if not is_in_session:
            return jsonify({"message": "You are not in the class for this attendance session"}), 403
            
        # Store student info in session
        session['student_id'] = student.StudentID
        session['student_name'] = student.StudentName
        session['student_email'] = student.StudentEmail
        
        return jsonify({"message": "Student login successful"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred during login"}), 500

# Get current student info (GET /api/students/current)
@api_bp.route('/api/students/current', methods=['GET'])
def current_student():
    try:
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({"message": "Not logged in"}), 401
            
        return jsonify({
            "student": {
                "id": session.get('student_id'),
                "name": session.get('student_name'),
                "email": session.get('student_email')
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred"}), 500

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
            
        # Find or create class
        class_obj = Class.query.filter_by(ClassName=class_name).first()
        if not class_obj:
            class_obj = Class(ClassName=class_name)
            db.session.add(class_obj)
            db.session.commit()
            
        # Create student
        new_student = Student(StudentName=name, StudentEmail=email)
        new_student.ClassIDInStudent = class_obj.ClassID
        db.session.add(new_student)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful! Please take your photo.',
            'student_id': new_student.StudentID
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred during registration.'}), 500

# Student photo registration (POST /api/students/<int:student_id>/photo)
@api_bp.route('/api/students/<int:student_id>/photo', methods=['POST'])
def student_register_photo(student_id):
    try:
        data = request.get_json()
        photo_b64 = data.get('photo')
        if not photo_b64:
            return jsonify({'message': 'Photo is required.'}), 400
            
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'message': 'Student not found.'}), 404
            
        # Save photo temporarily and extract face vector
        photo_data = base64.b64decode(photo_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
            temp_path = temp.name
            temp.write(photo_data)
            
        try:
            # Extract face vector and store it
            student.set_face_vector(temp_path)
            db.session.commit()
            
            # Clean up the temporary file
            os.unlink(temp_path)
            
            return jsonify({'message': 'Photo saved successfully!'}), 200
        except Exception as e:
            print(f"Face vector extraction error: {e}")
            os.unlink(temp_path)
            return jsonify({'message': 'Could not process face in photo. Please try again.'}), 400
            
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
        
    # Find subject ID
    subject = Subject.query.filter_by(
        SubjectName=module,
        TeacherIDInSubject=session['teacher_id']
    ).first()
    
    if not subject:
        return jsonify({'message': 'Subject not found for this teacher'}), 404
        
    # Get class associated with this subject
    class_id = subject.ClassIDInSubject
    
    # Fetch students filtered by class ID and group if specified
    if group.lower() == 'all':
        students = Student.query.filter_by(ClassIDInStudent=class_id).all()
    else:
        # In a real app, you would handle groups within a class
        # For now, we'll just filter by class
        students = Student.query.filter_by(ClassIDInStudent=class_id).all()
        
    attendance_session['active'] = True
    attendance_session['students'] = [
        {
            'id': s.StudentID, 
            'name': s.StudentName,
            'email': s.StudentEmail, 
            'selfRecorded': False, 
            'status': None
        }
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
        
    # In a real app, you would save attendance records to database here
    
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
    
    if status not in ['present', 'absent']:
        return jsonify({'message': 'Invalid status'}), 400
        
    found = False
    for s in attendance_session['students']:
        if s['id'] == student_id:
            s['status'] = status
            found = True
            break
            
    if not found:
        return jsonify({'message': 'Student not found in current session'}), 404
        
    return jsonify({'message': f'Student marked as {status}'}), 200

# Student self-attendance (POST /api/attendance-records)
@api_bp.route('/api/attendance-records', methods=['POST'])
def attendance_record():
    try:
        if not attendance_session['active']:
            return jsonify({"message": "No active attendance session"}), 403
            
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
            
        photo_b64 = data.get('photo')
        if not photo_b64:
            return jsonify({"message": "Invalid photo: photo not found"}), 400
            
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({"message": "Not authorized: please log in again"}), 401
            
        # Get the student from database
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"message": "Student not found"}), 404
            
        # Get stored face vector
        stored_vector = student.get_face_vector()
        if not stored_vector:
            return jsonify({"message": "No reference photo found for this student"}), 404
            
        # Save submitted photo temporarily for face comparison
        photo_data = base64.b64decode(photo_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
            temp_path = temp.name
            temp.write(photo_data)
            
        try:
            # Get face vector from submitted photo
            submitted_vector = get_face_vector(temp_path)
            
            # Compare face vectors
            is_match = compare_face_vectors(stored_vector, submitted_vector)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            if not is_match:
                return jsonify({"message": "Face verification failed. Please try again."}), 400
                
            # Mark attendance in the session
            for s in attendance_session['students']:
                if s['id'] == student_id:
                    s['selfRecorded'] = True
                    s['status'] = 'present'
                    break
                    
            return jsonify({"message": "Attendance recorded successfully"}), 200
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            print(f"Face verification error: {e}")
            return jsonify({"message": "Could not process face in photo. Please try again."}), 400
            
    except Exception as e:
        print(f"Error recording attendance: {e}")
        return jsonify({"message": "An error occurred while recording attendance"}), 500

# Get attendance records (GET /api/attendance-records)
@api_bp.route('/api/attendance-records', methods=['GET'])
def get_attendance_record():
    try:
        if 'teacher_id' not in session:
            return jsonify({"message": "Not authorized"}), 401
            
        if not attendance_session['active']:
            return jsonify({"message": "No active attendance session"}), 404
            
        return jsonify({"attendance_records": attendance_session['students']}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while fetching attendance records"}), 500

# Export attendance as Excel (coming soon)
# @api_bp.route('/api/attendance-records/export', methods=['GET'])
# def export_attendance():
#     pass
