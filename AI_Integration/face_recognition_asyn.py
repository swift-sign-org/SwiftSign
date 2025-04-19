import time
from deepface import DeepFace as Dp
import os
import cv2





def resize_image(path, size=(160, 160)):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image at path: {path}")
    img = cv2.resize(img, size)
    return img  # Return the resized image

model = Dp.build_model("ArcFace")

def is_same_person(img1_path, img2_path):
    try:
        img1 = resize_image(img1_path)
        img2 = resize_image(img2_path)
        result = Dp.verify(img1_path=img1_path, img2_path=img2_path, enforce_detection=False, model_name='ArcFace')
        return 'answer:',result['verified']
    except Exception as e:
        print(f"Error during verification: {e}")
        return False

def get_face_vector(img_path):
    try:
        img = resize_image(img_path)
        vector = Dp.represent(img, model_name='ArcFace')
        return vector
    except Exception as e:
        print(f"Error during face vector extraction: {e}")
        return None

if __name__ == "__main__":
    start = time.time()
    print("Start time:", start)


    # Use the correct full paths to your images
    img1_path = r'C:\Users\islam\SwiftSign\SwiftSign\1.jpg'
    
    vector = get_face_vector(img1_path)
    print(type(vector[0]))
    print("Face vector:", vector[0])


    print("Time:", round(time.time() - start, 2), "seconds")