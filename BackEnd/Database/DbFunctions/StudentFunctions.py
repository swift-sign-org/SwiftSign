from BackEnd.Database.ProjectDatabase import *


# Insert a new student into the database
def insertStudent(
        studentID,
        studentFirstName,
        studentLastName,
        studentEmail,
        studentPhoto,
        studentBirthDate,
        studentPhone,
        classIDInStudent
):
    with app.app_context():
        if not studentEmail.endswith("@hns-re2sd.dz"):
            print("❌ Error: Student email must end with '@hns-re2sd.dz'.")
            return

        newStudent = Student(
            StudentID = studentID,
            StudentFirstName = studentFirstName,
            StudentLastName = studentLastName,
            StudentEmail = studentEmail,
            StudentPhoto = studentPhoto,
            StudentBirthDate = studentBirthDate,
            StudentPhone = studentPhone,
            ClassIDInStudent = classIDInStudent
        )
        db.session.add(newStudent)
        db.session.commit()
        print(f"✅ Student {studentFirstName} {studentLastName} inserted successfully.")

# def insertStudent(studentID, studentFirstName, studentLastName, studentEmail, studentPhoto, studentBirthDate, studentPhone, classIDInStudent):
#     with app.app_context():
#         newStudent = Student(
#             StudentID = studentID,
#             StudentFirstName = studentFirstName,
#             StudentLastName = studentLastName,
#             StudentEmail = studentEmail,
#             StudentPhoto = studentPhoto,
#             StudentBirthDate = studentBirthDate,
#             StudentPhone = studentPhone,
#             ClassIDInStudent = classIDInStudent
#         )
#         db.session.add(newStudent)
#         db.session.commit()



# Update a student's information in the database
def updateStudentById(studentId, **kwargs):
    with app.app_context():
        student = Student.query.filter_by(StudentID=studentId).first()
        if student:
            for key, value in kwargs.items():
                if hasattr(student, key):
                    if key == "StudentEmail" and not value.endswith("@hns-re2sd.dz"):
                        print("❌ Error: Student email must end with '@hns-re2sd.dz'.")
                        return
                    setattr(student, key, value)
            db.session.commit()
            print(f"✅ Student with ID {studentId} updated successfully.")
        else:
            print(f"❌ No student found with ID {studentId}.")



# def updateStudentById(studentId, **kwargs):
#     with app.app_context():
#         student = Student.query.filter_by(StudentID=studentId).first()
#         if student:
#             for key, value in kwargs.items():
#                 if hasattr(student, key):
#                     setattr(student, key, value)
#             db.session.commit()
#             print(f"Student with ID {studentId} updated successfully.")
#         else:
#             print(f"No student found with ID {studentId}.")


# Delete a student from the database
def deleteStudentById(studentId):
    with app.app_context():
        student = Student.query.filter_by(StudentID=studentId).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            print(f"✅ Student with ID {studentId} deleted successfully.")
        else:
            print(f"❌ No student found with ID {studentId}.")

