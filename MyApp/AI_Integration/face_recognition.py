from deepface import DeepFace as Dp
from numpy import dot
from numpy.linalg import norm
import cv2

def verify_faces_existance(img_path):
    faces=Dp.extract_faces(img_path)
    if len(faces)==1:
        return True
    return False

def compare_face_vectors(vec1, vec2):
    vec1 = vec1[0]['embedding']
    vec2 = vec2[0]['embedding']
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def resize_image(path, size=(160, 160)):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image at: {path}")
    return cv2.resize(img, size)

def get_arcface_vector(img_path):
    try:
        Dp.build_model("ArcFace")  # Ensure model is initialized
        return Dp.represent(img_path=img_path, model_name='ArcFace', enforce_detection=False)
    except Exception as e:
        print(f"Vector extraction failed: {e}")
        return None

def cosine_similarity(vec1, vec2):
    vec1 = vec1[0]['embedding']
    vec2 = vec2[0]['embedding']
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def compare_faces_manual(img1_path, img2_path, threshold=0.35):
    vector1 = get_arcface_vector(img1_path)
    vector2 = get_arcface_vector(img2_path)
    if vector1 and vector2:
        similarity = cosine_similarity(vector1, vector2)
        return similarity > threshold, similarity
    return False, None


if __name__ == "__main__":
    # Example usage
    img1 = r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\1.jpg'
    img2 = r'C:\Users\islam\SwiftSign\SwiftSign\MyApp\2.jpg'

    match, similarity_score = compare_faces_manual(img1, img2)
    print("Match:", match)
    print("Cosine Similarity:", similarity_score)
