from BackEnd.Database.ProjectDatabase import *


# Insert a new teacher into the database
from datetime import datetime

def insertTeacher(
        teacherID,
        teacherFirstName,
        teacherLastName,
        teacherEmail,
        teacherBirthDate,
        teacherPhone
):
    if not teacherEmail.endswith("@hns-re2sd.dz"):
        print("❌ Error: This is not an HNS Account.")
        return

    # Convert the string date to a datetime.date object
    try:
        teacherBirthDate = datetime.strptime(teacherBirthDate, '%Y-%m-%d').date()
    except ValueError:
        print("❌ Error: Incorrect date format. Please use YYYY-MM-DD.")
        return

    newTeacher = Teacher(
        TeacherID=teacherID,
        TeacherFirstName=teacherFirstName,
        TeacherLastName=teacherLastName,
        TeacherEmail=teacherEmail,
        TeacherBirthDate=teacherBirthDate,
        TeacherPhone=teacherPhone
    )

    # Use a session to add and commit
    with app.app_context():
        db.session.add(newTeacher)
        try:
            db.session.commit()
            print(f"✅ Teacher {teacherFirstName} {teacherLastName} inserted successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error inserting teacher: {e}")
        finally:
            db.session.remove()




# def insertTeacher(teacherID, teacherFirstName, teacherLastName, teacherEmail, teacherBirthDate, teacherPhone):
#     with app.app_context():
#         newTeacher = Teacher(
#             TeacherID = teacherID,
#             TeacherFirstName = teacherFirstName,
#             TeacherLastName = teacherLastName,
#             TeacherEmail = teacherEmail,
#             TeacherBirthDate = teacherBirthDate,
#             TeacherPhone = teacherPhone
#         )
#         db.session.add(newTeacher)
#         db.session.commit()



# Update a teacher's information in the database
def updateTeacherById(teacherId, **kwargs):
    with app.app_context():
        teacher = Teacher.query.filter_by(TeacherID=teacherId).first()
        if teacher:
            for key, value in kwargs.items():
                if hasattr(teacher, key):
                    if key == "TeacherEmail" and not value.endswith("@hns-re2sd.dz"):
                        print("❌ Error: Teacher email must end with '@hns-re2sd.dz'.")
                        return
                    setattr(teacher, key, value)
            db.session.commit()
            print(f"✅ Teacher with ID {teacherId} updated successfully.")
        else:
            print(f"❌ No teacher found with ID {teacherId}.")



# def updateTeacherById(teacherId, **kwargs):
#     with app.app_context():
#         teacher = Teacher.query.filter_by(TeacherID=teacherId).first()
#         if teacher:
#             for key, value in kwargs.items():
#                 if hasattr(teacher, key):
#                     setattr(teacher, key, value)
#             db.session.commit()
#             print(f"Teacher with ID {teacherId} updated successfully.")
#         else:
#             print(f"No teacher found with ID {teacherId}.")


# Delete a teacher from the database
def deleteTeacherById(teacherId):
    with app.app_context():
        teacher = Teacher.query.filter_by(TeacherID=teacherId).first()
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
            print(f"✅ Teacher with ID {teacherId} deleted successfully.")
        else:
            print(f"❌ No teacher found with ID {teacherId}.")



# insertTeacher(
#     teacherID=101,
#     teacherFirstName="John",
#     teacherLastName="Doe",
#     teacherEmail="a.aa@hns-re2sd.dz",
#     teacherBirthDate="1990-01-01",
#     teacherPhone="1234567890"
# )

# updateTeacherById(2, TeacherEmail="b.b@hns-re2sd.dz")

# deleteTeacherById(2)