from flask import blueprints, request, jsonify


api_bp = blueprints.Blueprint('api', __name__)


@api_bp.route('/api/teacher_login', methods=['POST'])
def teacher_login():
    # Logic for teacher login
    return jsonify({"message": "Teacher login successful"}) 


@api_bp.route('/api/student_login', methods=['POST'])
def student_login():
    # Logic for student login
    return jsonify({"message": "Student login successful"})


@api_bp.route('/api/attendenceRecord', methods=['POST'])
def attendenceRecord():
    # Logic for attendance record
    return jsonify({"message": "Attendance record successful"})


@api_bp.route('/api/attendenceRecord', methods=['GET'])
def get_attendenceRecord():
    # Logic for getting attendance record
    return jsonify({"message": "Attendance record fetched successfully"})