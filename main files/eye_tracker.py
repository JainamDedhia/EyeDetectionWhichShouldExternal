import numpy as np
import pyautogui
import logging

# Screen and grid settings
screen_w, screen_h = pyautogui.size()
keyboard_start_y = screen_h // 2
grid_cols = 100
grid_rows = 30
key_width = screen_w // grid_cols
key_height = (screen_h // 2) // grid_rows
eye_movement_threshold = 0.03

def navigate_keyboard_by_grid(landmarks):
    try:
        left_eye = [landmarks[145], landmarks[159]]
        right_eye = [landmarks[374], landmarks[386]]

        avg_left_eye_y = (left_eye[0].y + left_eye[1].y) / 2
        avg_right_eye_y = (right_eye[0].y + right_eye[1].y) / 2
        avg_eye_y = (avg_left_eye_y + avg_right_eye_y) / 2

        avg_left_eye_x = (left_eye[0].x + left_eye[1].x) / 2
        avg_right_eye_x = (right_eye[0].x + right_eye[1].x) / 2
        avg_eye_x = (avg_left_eye_x + avg_right_eye_x) / 2

        eye_y_shift = avg_eye_y - 0.5
        eye_x_shift = avg_eye_x - 0.5

        cur_x, cur_y = pyautogui.position()

        if abs(eye_x_shift) > eye_movement_threshold:
            move_x = np.sign(eye_x_shift) * key_width
            cur_x = np.clip(cur_x + move_x, 0, screen_w)

        if abs(eye_y_shift) > eye_movement_threshold:
            move_y = np.sign(eye_y_shift) * key_height
            cur_y = np.clip(cur_y + move_y, keyboard_start_y, screen_h)

        pyautogui.moveTo(cur_x, cur_y)
    except Exception as e:
        logging.error("Error in eye navigation: %s", str(e))
