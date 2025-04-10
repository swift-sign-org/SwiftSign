# Here where we create the database and the tables
# This file is only for creating the database and the tables, we will not use it in the project.

# Import the necessary libraries
from flask_sqlalchemy import SQLAlchemy
from app import app


# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the Teacher table
class Teacher(db.Model):
    TeacherID = db.Column(db.Integer, primary_key=True, nullable=False)
    TeacherFirstName = db.Column(db.String(100), nullable=False)
    TeacherLastName = db.Column(db.String(100), nullable=False)
    TeacherEmail = db.Column(db.String(120), nullable=False)
    TeacherBirthDate = db.Column(db.Date, nullable=False)
    TeacherPhone = db.Column(db.String(120), nullable=False)

    # Relationship to Subject
    subjects = db.relationship('Subject', backref='teacher', cascade='all, delete', passive_deletes=True)

    def check_password(self, password):
        return self.TeacherPassword == password

# Define the Class table
class Class(db.Model):
    ClassID = db.Column(db.Integer, primary_key=True, nullable=False)
    ClassName = db.Column(db.String(100), nullable=False)
    ClassDescription = db.Column(db.String(200), nullable=False)

    # Relationship to Subject
    subjects = db.relationship('Subject', backref='class_', cascade='all, delete', passive_deletes=True)

    # Relationship to Student
    students = db.relationship('Student', backref='class_', cascade='all, delete', passive_deletes=True)

# Define the Subject table
class Subject(db.Model):
    SubjectID = db.Column(db.Integer, primary_key=True, nullable=False)
    SubjectName = db.Column(db.String(100), nullable=False)
    SubjectDescription = db.Column(db.String(200), nullable=False)
    TeacherIDInSubject = db.Column(db.Integer, db.ForeignKey('teacher.TeacherID', ondelete='CASCADE'), nullable=False)
    ClassIDInSubject = db.Column(db.Integer, db.ForeignKey('class.ClassID', ondelete='CASCADE'), nullable=False)

# Define the Student table
class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True, nullable=False)
    StudentFirstName = db.Column(db.String(100), nullable=False)
    StudentLastName = db.Column(db.String(100), nullable=False)
    StudentEmail = db.Column(db.String(120), nullable=False)
    StudentPhoto = db.Column(db.LargeBinary, nullable=False)
    StudentBirthDate = db.Column(db.Date, nullable=False)
    StudentPhone = db.Column(db.String(120), nullable=False)
    ClassIDInStudent = db.Column(db.Integer, db.ForeignKey('class.ClassID', ondelete='CASCADE'), nullable=False)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()