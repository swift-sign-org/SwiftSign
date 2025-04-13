import cv2
import numpy as np
import os
from datetime import datetime
from deepface import DeepFace as Dp

def is_same_person(img1,img2):
    result = Dp.verify(img1,img2,enforce_detection=False,model_name='ArcFace')
    return result['verified']


test= is_same_person('mohamed.png','ayoub.png')
print(test)