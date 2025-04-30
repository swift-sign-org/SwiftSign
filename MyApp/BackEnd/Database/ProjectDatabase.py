import json
import bcrypt
from flask_sqlalchemy import SQLAlchemy

from MyApp.AI_Integration.face_recognition import get_face_vector


db = SQLAlchemy()


# ==================== MODELS ====================

class Teacher(db.Model):
    TeacherID = db.Column(db.Integer, primary_key=True)
    TeacherName = db.Column(db.String(100))
    TeacherEmail = db.Column(db.String(120), unique=True)
    TeacherPassword = db.Column(db.String(120))

    subjects = db.relationship('Subject', backref='teacher', cascade='all, delete', passive_deletes=True)

    def __init__(self, TeacherName, TeacherEmail, Password):
        self.TeacherName = TeacherName
        self.TeacherEmail = TeacherEmail
        self.set_password(Password)

    def set_password(self, password):
        self.TeacherPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.TeacherPassword.encode('utf-8'))


class Class(db.Model):
    ClassID = db.Column(db.Integer, primary_key=True)
    ClassName = db.Column(db.String(100))

    subjects = db.relationship('Subject', backref='class_', cascade='all, delete', passive_deletes=True)
    students = db.relationship('Student', backref='class_', cascade='all, delete', passive_deletes=True)

    def __init__(self, ClassName):
        self.ClassName = ClassName


class Subject(db.Model):
    SubjectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SubjectName = db.Column(db.String(100))
    TeacherIDInSubject = db.Column(db.Integer, db.ForeignKey('teacher.TeacherID', ondelete='CASCADE'))
    ClassIDInSubject = db.Column(db.Integer, db.ForeignKey('class.ClassID', ondelete='CASCADE'))

    def __init__(self, SubjectName, TeacherIDInSubject, ClassIDInSubject):
        self.SubjectName = SubjectName
        self.TeacherIDInSubject = TeacherIDInSubject
        self.ClassIDInSubject = ClassIDInSubject


class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentName = db.Column(db.String(100))
    StudentEmail = db.Column(db.String(120), unique=True)
    StudentFaceVector = db.Column(db.Text)
    ClassIDInStudent = db.Column(db.Integer, db.ForeignKey('class.ClassID', ondelete='CASCADE'))

    def __init__(self, StudentName, StudentEmail):
        self.StudentName = StudentName
        self.StudentEmail = StudentEmail

    def set_face_vector(self, ImagePath):
        embedding = get_face_vector(ImagePath)
        self.StudentFaceVector = json.dumps(embedding)

    def get_face_vector(self):
        if self.StudentFaceVector:
            return json.loads(self.StudentFaceVector)
        return None


