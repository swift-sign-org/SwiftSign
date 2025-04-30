import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN warnings
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)  # Suppress TF deprecation

import cv2
import numpy as np
from datetime import datetime
from deepface import DeepFace as Dp
import threading
import time

# Configuration parameters
img_path = r'C:\Users\brency\face recognition\SwiftSign\AI-Integration\ayoub.png'
process_every_n_frames = 10  # Process every 10th frame for recognition
resolution = (640, 480)  # Lower resolution for faster processing

# Setup face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global variables for threading
frame_to_process = None
processing_result = False
processing_done = threading.Event()
stop_thread = threading.Event()

def is_same_person(img1, img2):
    if img1 is None or img2 is None:
        return False
    
    try:
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
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

def recognition_thread(db_face):
    global frame_to_process, processing_result, processing_done
    
    while not stop_thread.is_set():
        # Wait until we have a frame to process
        if frame_to_process is not None:
            # Extract face
            face_crop = frame_to_process
            # Release the lock
            frame_to_process = None
            
            # Do the actual recognition
            result = is_same_person(face_crop, db_face)
            
            # Set the result and signal completion
            processing_result = result
            processing_done.set()
        
        # Small sleep to prevent CPU hogging
        time.sleep(0.01)

# Initialize camera
def init_camera():
    for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
        try:
            cap = cv2.VideoCapture(0, backend)
            if cap.isOpened():
                # Set resolution
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
                return cap
        except Exception as e:
            print(f"Backend {backend} failed: {e}")
    
    return None

# Main program
def main():
    global frame_to_process, processing_result, processing_done
    
    # Load and verify DB image
    db_img = cv2.imread(img_path)
    if db_img is None:
        print(f"Error loading: {img_path}")
        return
    
    db_face = extract_face(db_img)
    if db_face is None:
        print("No face in DB image")
        return
    else:
        print("Reference face loaded successfully")
    
    # Initialize camera
    cap = init_camera()
    if not cap or not cap.isOpened():
        print("Error: Could not open camera with any backend")
        return
    
    # Start recognition thread
    recognition_thread_handle = threading.Thread(target=recognition_thread, args=(db_face,))
    recognition_thread_handle.daemon = True
    recognition_thread_handle.start()
    
    print("Starting face recognition... Press 'q' to quit")
    
    frame_count = 0
    matched = False
    
    while not matched:
        ret, frame = cap.read()
        if not ret:
            print("Frame capture error")
            break
        
        frame_count += 1
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
            
            # Process recognition every N frames and if not already processing
            if frame_count % process_every_n_frames == 0 and frame_to_process is None and not processing_done.is_set():
                face_crop = frame[y:y+h, x:x+w]
                frame_to_process = face_crop
            
        # Check if processing is done
        if processing_done.is_set():
            if processing_result:
                matched = True
                print(f"✅ Match at {datetime.now().strftime('%H:%M:%S')}")
                # Draw green rectangle for match
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            processing_done.clear()
        
        # Display the frame
        cv2.imshow('Webcam', frame)
        
        # Break on 'q' press
        if cv2.waitKey(1) == ord('q'):
            break
    
    # Cleanup
    stop_thread.set()
    if recognition_thread_handle.is_alive():
        recognition_thread_handle.join(timeout=1.0)
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()