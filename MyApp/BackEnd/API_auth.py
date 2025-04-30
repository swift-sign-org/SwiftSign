from flask import blueprints, jsonify, session, request
import base64
import os
import tempfile

from MyApp.BackEnd.Database.ProjectDatabase import db, Teacher, Student, Class, Subject


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
        teacher_password = request.get_json()['password']
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
            
            return jsonify({'message': 'Photo saved successfully!'}), 200
        except Exception as e:
            print(f"Face vector extraction error: {e}")
            return jsonify({'message': 'Could not process face in photo. Please try again.'}), 400
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred while saving the photo.'}), 500
