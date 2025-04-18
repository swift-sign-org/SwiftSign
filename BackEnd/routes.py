from flask import Blueprint, render_template, redirect, url_for, session, flash
from BackEnd.Database.ProjectDatabase import Student, db
from BackEnd.API import attendance_session  # Import the attendance session state

routes_blueprint = Blueprint('routes', __name__)


@routes_blueprint.route('/teacher-register')
def teacher_register():
    return render_template('teacherRegister.html')

@routes_blueprint.route('/student-register')
def student_register():
    return render_template('studentRegister.html')


@routes_blueprint.route('/teacher-login')
def teacher_login():
    return render_template('teacherLogin.html')


@routes_blueprint.route('/register')
def register():
    return render_template('register.html')

@routes_blueprint.route('/')
def student_login():
    # Block access if attendance is not started by the teacher
    if not attendance_session.get('active'):
        # Optionally, you can render a custom page or show a message
        return render_template('')
    return render_template('studentLogin.html')

@routes_blueprint.route('/attendance')
def student_attendance():
    # Block access if attendance is not started by the teacher
    if not attendance_session.get('active'):
        return render_template('studentCamera.html', blocked=True)
    return render_template('studentCamera.html', blocked=False)

@routes_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.teacher_login'))


@routes_blueprint.route('/teacher-dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session:
        return redirect(url_for('routes.teacher_login'))
    return render_template('teacherMainPage.html')


@routes_blueprint.route('/create-student')
def create_student():
    new_student = Student(StudentEmail="islam@hns-re2sd.dz", StudentName="islam")
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('routes.teacher_dashboard'))