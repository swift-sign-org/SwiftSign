from flask import Blueprint, request, jsonify, render_template, redirect, url_for


routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/admin')
def teacher_login():
    return render_template('teacher_login.html')


@routes_bp.route('/panel', methods=['POST'])
def teacher_panel():
    return render_template('panel.html')


@routes_bp.route('/')
def student_login():
    return render_template('student.html')


@routes_bp.route('/login', methods=['POST'])
def student_panel():
    return render_template('student_panel.html')