from flask import blueprints, jsonify, session, request

from app import app
from BackEnd.Database.ProjectDatabase import Teacher, Class, Subject, Student ,db

api_bp = blueprints.Blueprint('api', __name__)


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
        


@api_bp.route('/api/attendanceRecord', methods=['POST'])
def attendanceRecord():
    # Logic for attendance record
    try:
        student_photo = request.json['student_photo']
        student_id = session.get('student_id')
        database_photo = session.get('student_photo')
        attendance_status = request.json['attendance_status']
        if not student_photo :
            return jsonify({"message": "Invalid photo: photo not found"}), 401
        if student_photo != database_photo:
            return jsonify({"message": "Invalid photo: photo does not match"}), 401
        return jsonify({"message": "Attendance record successful"}), 200
        # and then here we add the record to the database
        # with db.session.begin():
        #     db.session.add(attendance_record)
        #     db.session.commit()
    except KeyError as e:
        print(e)
        return jsonify({"message": "An error occurred while recording attendance"}), 500

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while recording attendance"}), 500
    return jsonify({"message": "Attendance record successful"})


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
    