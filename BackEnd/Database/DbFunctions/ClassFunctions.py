from BackEnd.Database.ProjectDatabase import *

# Insert a new class into the database
def insertClass(classId, className, classDescription):
    with app.app_context():
        session = db.session
        newClass = Class(
            ClassID=classId,
            ClassName=className,
            ClassDescription=classDescription
        )
        session.add(newClass)
        try:
            session.commit()
            print(f"✅ Class '{className}' inserted successfully.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error inserting class: {e}")
        finally:
            session.remove()



# Update a class's information in the database
def updateClassById(classId, **kwargs):
    with app.app_context():
        class_ = Class.query.filter_by(ClassID=classId).first()
        if class_:
            for key, value in kwargs.items():
                if hasattr(class_, key):
                    setattr(class_, key, value)
            db.session.commit()
            print(f"Class with ID {classId} updated successfully.")
        else:
            print(f"No class found with ID {classId}.")


# Delete a class from the database
def deleteClassById(classId):
    with app.app_context():
        class_ = Class.query.filter_by(ClassID=classId).first()
        if class_:
            db.session.delete(class_)
            db.session.commit()
            print(f"✅ Class with ID {classId} deleted successfully.")
        else:
            print(f"❌ No class found with ID {classId}.")


insertClass(3, "Class 1", "Description of Class 1")