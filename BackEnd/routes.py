from flask import Blueprint, render_template, request, redirect, url_for, session, flash


routes_blueprint = Blueprint('routes', __name__)



@routes_blueprint.route('/teacher-login')
def teacher_login():
    return render_template('teacher-login.html')

@routes_blueprint.route('/')
def student_login():
    return render_template('studentLogin.html')

@routes_blueprint.route('/teacher-login')
def student_attendance():
    return render_template('student-attendance.html')

@routes_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.teacher_login'))


@routes_blueprint.route('/teacher-dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session:
        return redirect(url_for('routes.teacher_login'))
    return render_template('teacher-dashboard.html')
