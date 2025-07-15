# File: webcam.py
# Capture image from webcam and save to file

import cv2
import os
import time

def capture_image(output_path="captured.jpg"):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot access webcam")
        return None

    print("Press SPACE to capture, ESC to exit")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Webcam", frame)

        key = cv2.waitKey(1)
        if key % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif key % 256 == 32:
            # SPACE pressed
            cv2.imwrite(output_path, frame)
            print(f"Image saved to {output_path}")
            break

    cam.release()
    cv2.destroyAllWindows()
    return output_path
