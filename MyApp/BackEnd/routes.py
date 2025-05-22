from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from MyApp.BackEnd.Database.ProjectDatabase import Student, db
from MyApp.BackEnd.API_auth import attendance_session  # Import the attendance session state

routes_blueprint = Blueprint('routes', __name__)


@routes_blueprint.route('/register')
def teacher_register():
    return render_template('rejister.html')


@routes_blueprint.route('/register/face')
def register_face():
    # Check if student_id exists in the request or session
    student_id = request.args.get('student_id') or session.get('pending_face_registration')
    
    if not student_id:
        flash('Please complete registration first', 'error')
        return redirect(url_for('routes.student_login'))
        
    # Store the student_id in session to keep it available for the API call
    session['pending_face_registration'] = student_id
    
    return render_template('faceRegister.html', student_id=student_id)




@routes_blueprint.route('/teacher-login')
def teacher_login():
    return render_template('teacherLogin.html')



@routes_blueprint.route('/')
def student_login():
    # Block access if attendance is not started by the teacher
    if not attendance_session.get('active'):
        # Optionally, you can render a custom page or show a message
        return render_template('blocked.html')
    return render_template('StudentLogin.html')

@routes_blueprint.route('/attendance')
def student_attendance():
    # Block access if attendance is not started by the teacher
    if not attendance_session.get('active'):
        return redirect(url_for('routes.student_login'))
    return render_template('camera.html', blocked=False)

@routes_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.teacher_login'))


@routes_blueprint.route('/teacher-dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session:
        return redirect(url_for('routes.teacher_login'))
    return render_template('teacherMainPage.html')


