from MyApp import create_app
from MyApp.AI_Integration.face_recognition import get_arcface_vector, compare_face_vectors
from MyApp.BackEnd.Database.ProjectDatabase import db, Teacher, Student, Class, Subject, Teaching9
import random
import string
import os
import json

# Create Flask app and push application context
app = create_app()
app.app_context().push()

# Function to generate random passwords
def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Function to save data to a text file
def save_to_file(data, filename="test_data.txt"):
    with open(filename, "w") as f:
        f.write(data)
    print(f"Data saved to {filename}")

def create_test_data():
    # Clear existing data from the tables
    Teaching9.query.delete()
    Subject.query.delete()
    Student.query.delete()
    Teacher.query.delete()
    Class.query.delete()
    
    db.session.commit()
    print("Database cleared.")
    
    data_text = "SwiftSign Test Data\n"
    data_text += "===================\n\n"
    
    # Create classes (groups)
    classes = [
        "L3 GL", "L3 SCI", "L3 STIW", "L2 MI", "L2 GL", "M1 SIC", 
        "M1 RSSI", "M2 SIC", "M2 RSSI"
    ]
    
    class_objects = {}
    
    data_text += "CLASSES\n-------\n"
    for class_name in classes:
        new_class = Class(class_name)
        db.session.add(new_class)
        db.session.flush()  # Get ID before committing
        class_objects[class_name] = new_class
        data_text += f"Class ID: {new_class.ClassID}, Name: {class_name}\n"
    
    # Create teachers
    teachers = [
        ("Ahmed", "Benali", "a.benali@hns-re2sd.dz"),
        ("Mohammed", "Cherif", "m.cherif@hns-re2sd.dz"),
        ("Karima", "Lahlou", "k.lahlou@hns-re2sd.dz"),
        ("Fatima", "Meziane", "f.meziane@hns-re2sd.dz"),
        ("Youcef", "Hadj", "y.hadj@hns-re2sd.dz")
    ]
    
    teacher_objects = {}
    
    data_text += "\nTEACHERS\n--------\n"
    for first_name, last_name, email in teachers:
        password = generate_password()
        new_teacher = Teacher(first_name, last_name, email, password)
        db.session.add(new_teacher)
        db.session.flush()  # Get ID before committing
        teacher_objects[email] = new_teacher
        data_text += f"Teacher ID: {new_teacher.TeacherID}, Name: {first_name} {last_name}, Email: {email}, Password: {password}\n"
    
    # Create subjects
    subjects = [
        "Python Programming", "Data Structures", "Algorithms", "Web Development",
        "Database Systems", "Computer Networks", "AI Fundamentals", "Machine Learning",
        "Software Engineering", "Operating Systems", "Computer Architecture"
    ]
    
    data_text += "\nSUBJECTS\n--------\n"
    for subject_name in subjects:
        # Assign random teacher to each subject
        random_teacher = random.choice(list(teacher_objects.values()))
        new_subject = Subject(subject_name, random_teacher.TeacherID)
        db.session.add(new_subject)
        db.session.flush()
        data_text += f"Subject ID: {new_subject.SubjectID}, Name: {subject_name}, Teacher: {random_teacher.TeacherFirstName} {random_teacher.TeacherLastName}\n"
    
    # Assign teachers to classes (Teaching9)
    data_text += "\nTEACHER-CLASS ASSIGNMENTS\n------------------------\n"
    for teacher in teacher_objects.values():
        # Assign 1-3 random classes to each teacher
        num_classes = random.randint(1, 3)
        assigned_classes = random.sample(list(class_objects.values()), num_classes)
        
        for class_obj in assigned_classes:
            teaching = Teaching9(teacher.TeacherID, class_obj.ClassID)
            db.session.add(teaching)
            db.session.flush()
            data_text += f"Teaching ID: {teaching.TeachingID}, Teacher: {teacher.TeacherFirstName} {teacher.TeacherLastName}, Class: {class_obj.ClassName}\n"
    
    # Create students (with face vectors from sample images)
    students = [
        ("Amina", "Khalidi", "a.khalidi@hns-re2sd.dz", "L3 GL"),
        ("Karim", "Boudjemaa", "k.boudjemaa@hns-re2sd.dz", "L3 GL"),
        ("Samira", "Hamid", "s.hamid@hns-re2sd.dz", "L3 SCI"),
        ("Omar", "Benkadi", "o.benkadi@hns-re2sd.dz", "L3 SCI"),
        ("Leila", "Messaoudi", "l.messaoudi@hns-re2sd.dz", "L3 STIW"),
        ("Tarek", "Zitouni", "t.zitouni@hns-re2sd.dz", "L3 STIW"),
        ("Nadia", "Hamdani", "n.hamdani@hns-re2sd.dz", "L2 MI"),
        ("Younes", "Allaoui", "y.allaoui@hns-re2sd.dz", "L2 MI"),
        ("Imane", "Behidj", "i.behidj@hns-re2sd.dz", "L2 GL"),
        ("Hassan", "Amrani", "h.amrani@hns-re2sd.dz", "L2 GL"),
        ("Yasmine", "Ouadah", "y.ouadah@hns-re2sd.dz", "M1 SIC"),
        ("Rachid", "Mansouri", "r.mansouri@hns-re2sd.dz", "M1 SIC"),
        ("Amel", "Zerrouki", "a.zerrouki@hns-re2sd.dz", "M1 RSSI"),
        ("Bilal", "Khelifi", "b.khelifi@hns-re2sd.dz", "M1 RSSI"),
        ("Djamel", "Boudiaf", "d.boudiaf@hns-re2sd.dz", "M2 SIC"),
        ("Naima", "Benramdane", "n.benramdane@hns-re2sd.dz", "M2 RSSI")
    ]
    
    data_text += "\nSTUDENTS\n--------\n"
    # Use provided sample images for face vectors
    sample_images = [
        r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\1.jpg',
        r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\2.jpg',
        r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\AI_Integration\3.jpg'
    ]
    
    for first_name, last_name, email, class_name in students:
        new_student = Student(first_name, last_name, email)
        new_student.set_class(class_objects[class_name].ClassID)
        
        # Set a face vector from one of the sample images
        image_path = random.choice(sample_images)
        try:
            face_vector = get_arcface_vector(image_path)
            new_student.StudentFaceVector = json.dumps(face_vector.tolist())
        except Exception as e:
            print(f"Could not set face vector for {email}: {e}")
        
        db.session.add(new_student)
        db.session.flush()
        data_text += f"Student ID: {new_student.StudentID}, Name: {first_name} {last_name}, Email: {email}, Class: {class_name}\n"
    
    # Commit all changes
    db.session.commit()
    print("Database populated with test data.")
    
    return data_text

if __name__ == "__main__":
    # Create test data and save to file
    test_data = create_test_data()
    save_to_file(test_data)
    
    # Optionally run face recognition test
    # a = get_arcface_vector(r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\1.jpg')
    # b = get_arcface_vector(r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\2.jpg')
    # print(compare_face_vectors(a, b))