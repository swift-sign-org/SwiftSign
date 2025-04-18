import cv2
import os
from deepface import DeepFace as Dp
import time


class test_context:
    def __enter__(self):
        # Initialize resources or setup
        print("Entering context")
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        end_time = time.time()
        print(f"Time taken: {end_time - self.start_time} seconds")

def is_same_person(img1, img2):
    if not os.path.exists(img1):
        print(f"File not found: {img1}")
        return False
    if not os.path.exists(img2):
        print(f"File not found: {img2}")
        return False
    result = Dp.verify(img1, img2, enforce_detection=False, model_name='ArcFace')
    return result['verified']

if __name__ == "__main__":
    with test_context() as tc:
        test = is_same_person(r'C:\Users\islam\SwiftSign\SwiftSign\2.jpg', r'C:\Users\islam\SwiftSign\SwiftSign\1.jpg')
        print(test)