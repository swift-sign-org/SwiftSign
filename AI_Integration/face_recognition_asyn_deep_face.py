from deepface import DeepFace as Dp
import cv2

def verify_faces_arcface(img1_path, img2_path):
    try:
        result = Dp.verify(img1_path=img1_path, img2_path=img2_path,
                           model_name='ArcFace', enforce_detection=False)
        return result['verified'], result['distance']
    except Exception as e:
        print(f"Verification failed: {e}")
        return False, None

# Example usage
img1 = r'C:\Users\islam\SwiftSign\SwiftSign\1.jpg'
img2 = r'C:\Users\islam\SwiftSign\SwiftSign\2.jpg'

is_verified, distance = verify_faces_arcface(img1, img2)
print("Verified:", is_verified)
print("Distance (lower is better):", distance)
