# create_db.py

# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

# Print current working directory
print("Current working directory:", os.getcwd())

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'SwiftSignDB.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bcrypt and SQLAlchemy init
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Models
class Teacher(db.Model):
    TeacherID = db.Column(db.Integer, primary_key=True, nullable=False)
    TeacherFirstName = db.Column(db.String(100), nullable=False)
    TeacherLastName = db.Column(db.String(100), nullable=False)
    TeacherEmail = db.Column(db.String(120), nullable=False)
    TeacherBirthDate = db.Column(db.Date, nullable=False)
    TeacherPhone = db.Column(db.String(120), nullable=False)
    TeacherPassword = db.Column(db.String(120), nullable=False)

    subjects = db.relationship('Subject', backref='teacher', cascade='all, delete', passive_deletes=True)

    def set_password(self, password):
        self.TeacherPassword = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.TeacherPassword, password)

class Class(db.Model):
    ClassID = db.Column(db.Integer, primary_key=True, nullable=False)
    ClassName = db.Column(db.String(100), nullable=False)
    ClassDescription = db.Column(db.String(200), nullable=False)

    subjects = db.relationship('Subject', backref='class_', cascade='all, delete', passive_deletes=True)
    students = db.relationship('Student', backref='class_', cascade='all, delete', passive_deletes=True)

class Subject(db.Model):
    SubjectID = db.Column(db.Integer, primary_key=True, nullable=False)
    SubjectName = db.Column(db.String(100), nullable=False)
    SubjectDescription = db.Column(db.String(200), nullable=False)
    TeacherIDInSubject = db.Column(db.Integer, db.ForeignKey('teacher.TeacherID', ondelete='CASCADE'), nullable=False)
    ClassIDInSubject = db.Column(db.Integer, db.ForeignKey('class.ClassID', ondelete='CASCADE'), nullable=False)

class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True, nullable=False)
    StudentFirstName = db.Column(db.String(100), nullable=False)
    StudentLastName = db.Column(db.String(100), nullable=False)
    StudentEmail = db.Column(db.String(120), nullable=False)
    StudentPhoto = db.Column(db.LargeBinary, nullable=False)
    StudentBirthDate = db.Column(db.Date, nullable=False)
    StudentPhone = db.Column(db.String(120), nullable=False)
    ClassIDInStudent = db.Column(db.Integer, db.ForeignKey('class.ClassID', ondelete='CASCADE'), nullable=False)

# Run
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Database and tables created successfully at", app.config['SQLALCHEMY_DATABASE_URI'])
