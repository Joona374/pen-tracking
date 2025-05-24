import cv2
import numpy as np

def get_cap():
    cap = cv2.VideoCapture(1)  # Try 0, 1, 2... but 1 seems to be yours
    if not cap.isOpened():
        print("Error: Could not open video device")
        exit()

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cap

def get_green_mask(hsv_frame) -> np.ndarray:
    lower_green = np.array((40, 30, 30))
    upper_green = np.array((90, 255, 255))

    mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    # Clean up the mask:
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask