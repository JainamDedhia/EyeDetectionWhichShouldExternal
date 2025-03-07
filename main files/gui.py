from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLineEdit, QPushButton
)
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor, QFont
import sys
import cv2

class EyeTrackerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eye-Controlled Keyboard")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("background-color: #1E1E2E; color: white;")

        # Layouts: Main Horizontal
        main_layout = QHBoxLayout()

        # Left: Camera Feed
        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setStyleSheet("border: 3px solid cyan; border-radius: 10px;")
        main_layout.addWidget(self.camera_label)

        # Right: Virtual Keyboard & Textbox
        right_layout = QVBoxLayout()

        # Textbox
        self.text_field = QLineEdit(self)
        self.text_field.setPlaceholderText("Your text appears here...")
        self.text_field.setStyleSheet("""
            background-color: #2E2E3E; color: white;
            padding: 10px; border: 2px solid cyan; border-radius: 8px;
            font-size: 18px;
        """)
        right_layout.addWidget(self.text_field)

        # Virtual Keyboard
        self.keyboard_layout = QGridLayout()
        self.add_virtual_keyboard()
        right_layout.addLayout(self.keyboard_layout)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        # Blink State
        self.blink_detected = False

    def update_frame(self, frame):
        """ Update the camera feed with overlays """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        qimg = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(qimg)

        # Add Blink Overlay
        if self.blink_detected:
            pixmap = self.add_blink_overlay(pixmap)

        self.camera_label.setPixmap(pixmap)

    def add_blink_overlay(self, pixmap):
        """ Draws a red blink indicator on the frame """
        painter = QPainter(pixmap)
        painter.setPen(QColor("red"))
        painter.setFont(QFont("Arial", 24))
        painter.drawText(20, 50, "BLINK DETECTED!")
        painter.end()
        return pixmap

    def set_blink_detected(self, detected):
        self.blink_detected = detected

    def add_virtual_keyboard(self):
        """ Create a virtual keyboard layout """
        keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '←']
        ]

        for row_idx, row in enumerate(keys):
            for col_idx, key in enumerate(row):
                btn = QPushButton(key)
                btn.setFixedSize(60, 60)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3A3A4A; color: white;
                        border: 2px solid cyan; border-radius: 8px;
                        font-size: 22px;
                    }
                    QPushButton:hover {
                        background-color: cyan; color: black;
                    }
                """)
                btn.clicked.connect(lambda _, k=key: self.handle_keypress(k))
                self.keyboard_layout.addWidget(btn, row_idx, col_idx)

    def handle_keypress(self, key):
        """ Handle key press and update text field """
        if key == '←':
            current_text = self.text_field.text()
            self.text_field.setText(current_text[:-1])
        else:
            self.text_field.setText(self.text_field.text() + key)

def launch_gui():
    app = QApplication(sys.argv)
    window = EyeTrackerGUI()
    window.show()
    return app, window
