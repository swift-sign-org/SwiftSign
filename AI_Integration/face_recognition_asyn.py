import time
from deepface import DeepFace as Dp
import cv2
from numpy import dot
from numpy.linalg import norm



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
    
def compare_face_vectors(vector1, vector2, threshold=0.35):
    try:
        # If DeepFace.represent returns a list of dicts, extract the 'embedding'
        if isinstance(vector1, list) and isinstance(vector2, list):
            vector1 = vector1[0]['embedding']
            vector2 = vector2[0]['embedding']
        similarity = dot(vector1, vector2) / (norm(vector1) * norm(vector2))
        return similarity > threshold
    except Exception as e:
        print(f"Error during face vector comparison: {e}")
        return False

if __name__ == "__main__":
    start = time.time()
    print("Start time:", start)


    # Use the correct full paths to your images
    img1_path = r'C:\Users\islam\SwiftSign\SwiftSign\1.jpg'
    vector1 = get_face_vector(img1_path)
    
    img2_path = r'C:\Users\islam\SwiftSign\SwiftSign\2.jpg'
    vector2 = get_face_vector(img2_path)

    print(compare_face_vectors(vector1, vector2))


    print("Time:", round(time.time() - start, 2), "seconds")