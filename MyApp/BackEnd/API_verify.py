from flask import blueprints, jsonify, session, request
from datetime import datetime
import base64
import os
import tempfile
from MyApp.AI_Integration.face_recognition import get_face_vector, compare_face_vectors
from MyApp.BackEnd.Database.ProjectDatabase import db, Teacher, Student, Class, Subject
from MyApp.BackEnd.API_auth import attendance_session

# Create a new blueprint for verification-related endpoints
verify_bp = blueprints.Blueprint('verify', __name__)

# Start attendance session (POST /api/attendance/start)
@verify_bp.route('/api/attendance/start', methods=['POST'])
def start_attendance():
    try:
        teacher_id = session.get('teacher_id')
        if not teacher_id:
            return jsonify({"message": "Teacher not logged in"}), 401
            
        data = request.get_json()
        module = data.get('module')
        group = data.get('group')
        
        if not module or not group:
            return jsonify({"message": "Module and group are required"}), 400
            
        # Check if attendance is already active
        if attendance_session['active']:
            return jsonify({
                "message": "An attendance session is already in progress",
                "session": {
                    "module": attendance_session['module'],
                    "group": attendance_session['group']
                }
            }), 409
            
        # Find class for this group
        class_obj = Class.query.filter_by(ClassName=group).first()
        if not class_obj:
            return jsonify({"message": f"Class '{group}' not found"}), 404
            
        # Get students in this class
        students = Student.query.filter_by(ClassIDInStudent=class_obj.ClassID).all()
        student_list = [{
            "id": student.StudentID,
            "name": student.StudentName,
            "email": student.StudentEmail,
            "selfRecorded": False,
            "status": "absent"  # Initial status
        } for student in students]
        
        # Start attendance session
        attendance_session.update({
            'active': True,
            'students': student_list,
            'module': module,
            'group': group,
            'start_time': datetime.now()
        })
        
        return jsonify({
            "message": "Attendance session started",
            "session": {
                "module": module,
                "group": group,
                "students": len(student_list)
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred starting attendance"}), 500

# End attendance session (POST /api/attendance/end)
@verify_bp.route('/api/attendance/end', methods=['POST'])
def end_attendance():
    try:
        teacher_id = session.get('teacher_id')
        if not teacher_id:
            return jsonify({"message": "Teacher not logged in"}), 401
            
        # Check if attendance is active
        if not attendance_session['active']:
            return jsonify({"message": "No active attendance session"}), 400
            
        # Get attendance records
        records = []
        for student in attendance_session['students']:
            records.append({
                "id": student['id'],
                "name": student['name'],
                "email": student['email'],
                "status": student['status'],
                "selfRecorded": student['selfRecorded']
            })
            
        # Save attendance records to database (implement this)
        # For now, just log them
        print(f"Attendance records for {attendance_session['module']} - {attendance_session['group']}:")
        for record in records:
            print(f"  {record['name']} ({record['email']}): {record['status']}")
            
        # Reset attendance session
        module = attendance_session['module']
        group = attendance_session['group']
        start_time = attendance_session['start_time']
        duration = (datetime.now() - start_time).total_seconds() / 60  # Duration in minutes
        
        attendance_session.update({
            'active': False,
            'students': [],
            'module': None,
            'group': None,
            'start_time': None
        })
        
        return jsonify({
            "message": "Attendance session ended",
            "session": {
                "module": module,
                "group": group,
                "duration": f"{duration:.1f} minutes",
                "records": records
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred ending attendance"}), 500

# Get student list in attendance session (GET /api/attendance/students)
@verify_bp.route('/api/attendance/students', methods=['GET'])
def attendance_students():
    try:
        teacher_id = session.get('teacher_id')
        if not teacher_id:
            return jsonify({"message": "Teacher not logged in"}), 401
            
        # Check if attendance is active
        if not attendance_session['active']:
            return jsonify({"message": "No active attendance session"}), 400
            
        # Return student list
        return jsonify({
            "session": {
                "module": attendance_session['module'],
                "group": attendance_session['group'],
                "students": attendance_session['students']
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred retrieving students"}), 500

# Mark attendance with facial recognition (POST /api/attendance)
@verify_bp.route('/api/attendance', methods=['POST'])
def mark_attendance():
    try:
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({"message": "Student not logged in"}), 401
            
        # Check if attendance is active
        if not attendance_session['active']:
            return jsonify({"message": "No active attendance session"}), 403
            
        # Get student data
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"message": "Student not found"}), 404
            
        # Process photo for face recognition
        data = request.get_json()
        photo_b64 = data.get('photo')
        if not photo_b64:
            return jsonify({'message': 'Photo is required.'}), 400
            
        # Save photo temporarily
        photo_data = base64.b64decode(photo_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
            temp_path = temp.name
            temp.write(photo_data)
            
        try:
            # Extract face vector from uploaded photo
            new_face_vector = get_face_vector(temp_path)
            
            # Compare with stored face vector
            stored_face_vector = student.get_face_vector()
            if stored_face_vector is None:
                os.unlink(temp_path)
                return jsonify({'message': 'No reference photo for comparison.'}), 400
                
            match, similarity = compare_face_vectors(new_face_vector, stored_face_vector)
            
            # Clean up the temporary file
            os.unlink(temp_path)
            
            if not match:
                return jsonify({
                    'message': 'Face does not match registered student.',
                    'similarity': similarity
                }), 403
                
            # Update attendance record
            for i, s in enumerate(attendance_session['students']):
                if s['id'] == student_id:
                    attendance_session['students'][i]['status'] = 'present'
                    attendance_session['students'][i]['selfRecorded'] = True
                    break
                    
            return jsonify({
                'message': 'Attendance marked successfully!',
                'similarity': similarity
            }), 200
            
        except Exception as e:
            print(f"Face recognition error: {e}")
            os.unlink(temp_path)
            return jsonify({'message': f'Face recognition error: {str(e)}'}), 400
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred marking attendance.'}), 500

# Get attendance records for a specific session (GET /api/attendance/record)
@verify_bp.route('/api/attendance/record', methods=['GET'])
def attendance_record():
    try:
        teacher_id = session.get('teacher_id')
        if not teacher_id:
            return jsonify({"message": "Teacher not logged in"}), 401
            
        # Check if attendance is active
        if not attendance_session['active']:
            return jsonify({"message": "No active attendance session"}), 400
            
        # Get current records
        records = []
        for student in attendance_session['students']:
            records.append({
                "id": student['id'],
                "name": student['name'],
                "email": student['email'],
                "status": student['status'],
                "selfRecorded": student['selfRecorded']
            })
            
        return jsonify({
            "session": {
                "module": attendance_session['module'],
                "group": attendance_session['group'],
                "records": records
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred retrieving attendance records"}), 500

# Get past attendance records (placeholder)
@verify_bp.route('/api/attendance/history', methods=['GET'])
def get_attendance_record():
    try:
        teacher_id = session.get('teacher_id')
        if not teacher_id:
            return jsonify({"message": "Teacher not logged in"}), 401
            
        # This would query the database for stored attendance records
        # Placeholder implementation returns empty list
        return jsonify({
            "history": []
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred retrieving attendance history"}), 500

# New endpoints using the verify_bp blueprint

# Verify student identity
@verify_bp.route('/verify/student', methods=['POST'])
def verify_student():
    try:
        data = request.get_json()
        student_email = data.get('email')
        photo_b64 = data.get('photo')
        
        if not student_email or not photo_b64:
            return jsonify({'message': 'Email and photo are required.'}), 400
            
        # Find student
        student = Student.query.filter_by(StudentEmail=student_email).first()
        if not student:
            return jsonify({'message': 'Student not found.'}), 404
            
        # Save photo temporarily
        photo_data = base64.b64decode(photo_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
            temp_path = temp.name
            temp.write(photo_data)
            
        try:
            # Extract face vector from uploaded photo
            new_face_vector = get_face_vector(temp_path)
            
            # Compare with stored face vector
            stored_face_vector = student.get_face_vector()
            if stored_face_vector is None:
                os.unlink(temp_path)
                return jsonify({'message': 'No reference photo for comparison.'}), 400
                
            match, similarity = compare_face_vectors(new_face_vector, stored_face_vector)
            
            # Clean up the temporary file
            os.unlink(temp_path)
            
            return jsonify({
                'verified': match,
                'similarity': similarity,
                'student': {
                    'id': student.StudentID,
                    'name': student.StudentName,
                    'email': student.StudentEmail
                }
            }), 200
            
        except Exception as e:
            print(f"Face verification error: {e}")
            os.unlink(temp_path)
            return jsonify({'message': f'Face verification error: {str(e)}'}), 400
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred during verification.'}), 500

# Get verification status
@verify_bp.route('/verify/status', methods=['GET'])
def verify_status():
    try:
        return jsonify({
            'status': 'operational',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred checking verification status.'}), 500