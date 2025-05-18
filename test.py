from MyApp import create_app
from MyApp.AI_Integration.face_recognition import get_arcface_vector, compare_face_vectors
# from MyApp.BackEnd.Database.ProjectDatabase import *
app = create_app()

if __name__ == "__main__":
    a = get_arcface_vector(r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\1.jpg')
    b = get_arcface_vector(r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\2.jpg')

    print(a)
    print(b)
    print(compare_face_vectors(a, b))