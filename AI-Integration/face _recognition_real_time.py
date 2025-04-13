import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN warnings
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)  # Suppress TF deprecation

import cv2
import numpy as np
from datetime import datetime
from deepface import DeepFace as Dp

img_path = 'ayoub.png'
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = None
for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
    try:
        cap = cv2.VideoCapture(0, backend)
        if cap.isOpened():
            break
    except Exception as e:
        print(f"Backend {backend} failed: {e}")
        
if not cap or not cap.isOpened():
    print("Error: Could not open camera with any backend")
    exit()

def is_same_person(img1, img2):
    if img1 is None or img2 is None:
        return False
    
    
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    try:
        result = Dp.verify(img1_rgb, img2_rgb, enforce_detection=False, model_name='ArcFace')
        return result['verified']
    except Exception as e:
        print(f"Verification error: {e}")
        return False

def extract_face(img):
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    
    if len(faces) > 0:
        x, y, w, h = faces[0]  
        return img[y:y+h, x:x+w]
    else:
        return None

# Load and verify DB image
db_img = cv2.imread(img_path)
if db_img is None:
    print(f"Error loading: {img_path}")
    exit()

db_face = extract_face(db_img)
if db_face is None:
    print("No face in DB image")
    exit()
else:
    print("Reference face loaded successfully")

print("Starting face recognition... Press 'q' to quit")

while True:
    matched=False
    ret, frame = cap.read()
    if not ret:
        print("Frame capture error")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        face_crop = frame[y:y+h, x:x+w]
        
        if is_same_person(face_crop, db_face):
            matched=True
            print(f"✅ Match at {datetime.now().strftime('%H:%M:%S')}")
            break
    
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord('q') or matched:
        break

cap.release()
cv2.destroyAllWindows()