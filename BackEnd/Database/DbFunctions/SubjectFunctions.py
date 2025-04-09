from BackEnd.Database.ProjectDatabase import *


# Insert a new subject into the database
def insertSubject(subjectID, subjectName, subjectDescription, teacherIDInSubject, classIDInSubject):
    with app.app_context():
        session = db.session
        newSubject = Subject(
            SubjectID=subjectID,
            SubjectName=subjectName,
            SubjectDescription=subjectDescription,
            TeacherIDInSubject=teacherIDInSubject,
            ClassIDInSubject=classIDInSubject
        )
        session.add(newSubject)
        try:
            session.commit()
            print(f"✅ Subject '{subjectName}' inserted successfully.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error inserting subject: {e}")
        finally:
            session.remove()




# Update a subject's information in the database
def updateSubjectById(subjectId, **kwargs):
    with app.app_context():
        subject = Subject.query.filter_by(SubjectID=subjectId).first()
        if subject:
            for key, value in kwargs.items():
                if hasattr(subject, key):
                    setattr(subject, key, value)
            db.session.commit()
            print(f"Subject with ID {subjectId} updated successfully.")
        else:
            print(f"No subject found with ID {subjectId}.")


# Delete a subject from the database
def deleteSubjectById(subjectId):
    with app.app_context():
        subject = Subject.query.filter_by(SubjectID=subjectId).first()
        if subject:
            db.session.delete(subject)
            db.session.commit()
            print(f"✅ Subject with ID {subjectId} deleted successfully.")
        else:
            print(f"❌ No subject found with ID {subjectId}.")


# insertSubject(2, "Math", "Mathematics subject", 2, 1)
deleteSubjectById(1)
deleteSubjectById(2)