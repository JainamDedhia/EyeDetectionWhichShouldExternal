import cv2
import mediapipe as mp
import dlib
import os
import logging
import math

def initialize_camera():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        logging.critical("Failed to open camera.")
        raise RuntimeError("Camera not accessible. Check if it's connected and available.")
    return cam

def initialize_face_mesh():
    mp_face_mesh = mp.solutions.face_mesh
    return mp_face_mesh.FaceMesh(refine_landmarks=True)

def initialize_dlib():
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    if not os.path.isfile(predictor_path):
        logging.critical(f"Missing file: {predictor_path}. Download it from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        raise FileNotFoundError(f"{predictor_path} not found. Ensure the file is available.")
    
    try:
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(predictor_path)
        return detector, predictor
    except Exception as e:
        logging.critical("Failed to load Dlib models: %s", str(e))
        raise e

def midpoint(point1, point2):
    return (point1.x + point2.x) / 2, (point1.y + point2.y) / 2

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_blink_ratio(eye_points, facial_landmarks):
    try:
        corner_left = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        corner_right = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)

        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

        horizontal_length = euclidean_distance(corner_left, corner_right)
        vertical_length = euclidean_distance(center_top, center_bottom)

        return horizontal_length / vertical_length
    except Exception as e:
        logging.error("Error in calculating blink ratio: %s", str(e))
        return
