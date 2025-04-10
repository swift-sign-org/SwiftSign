from flask import blueprints, jsonify, session, request

from app import app
from BackEnd.Database.ProjectDatabase import Teacher, Class, Subject, Student

api_bp = blueprints.Blueprint('api', __name__)


@api_bp.route('/api/teacher_login', methods=['POST'])
def teacher_login():
    # Logic for teacher 


    return jsonify({"message": "Teacher login successful"}) 


@api_bp.route('/api/student_login', methods=['POST'])
def student_login():
    # Logic for student login
    return jsonify({"message": "Student login successful"})


@api_bp.route('/api/attendanceRecord', methods=['POST'])
def attendanceRecord():
    # Logic for attendance record
    return jsonify({"message": "Attendance record successful"})


@api_bp.route('/api/attendanceRecord', methods=['GET'])
def get_attendanceRecord():
    # Logic for getting attendance record
    return jsonify({"message": "Attendance record fetched successfully"})