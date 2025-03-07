import pyautogui
import logging
from utils import get_blink_ratio
import time

BLINK_RATIO_THRESHOLD = 5.7
left_eye_landmarks = [36, 37, 38, 39, 40, 41]
right_eye_landmarks = [42, 43, 44, 45, 46, 47]
double_blink_interval = 1.0
def detect_blink(gray_frame, detector, predictor):
    faces = detector(gray_frame)
    if not faces:
        logging.warning("No faces detected.")
        return False
    
    for face in faces:
        landmarks = predictor(gray_frame, face)

        left_eye_ratio = get_blink_ratio(left_eye_landmarks, landmarks)
        right_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
        blink_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blink_ratio > BLINK_RATIO_THRESHOLD:
            logging.info("Blink detected. Performing click.")
            pyautogui.click()
            return True
    return False
    
