import cv2
import numpy as np
from utils import get_cap, get_green_mask

cap = get_cap()

drawing_points = []
current_drawing_color = (0, 0, 255)
capture_points = False
start_new_line = True

while True:
    ret, frame = cap.read()
    cropped_frame = frame[0:710, 380:870]
    
    if not ret:
        print("Failed to read frame")
        break
    
    hsv_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
    mask = get_green_mask(hsv_frame)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        biggest = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, [biggest], -1, (0, 255, 0), 3)
        M = cv2.moments(biggest)
        if M["m00"]:
            center_x = int(M["m10"]/M["m00"])
            center_y = int(M["m01"]/M["m00"])
            cv2.circle(frame, (center_x, center_y), 3, (0, 0, 0), -1)
            if capture_points:
                if start_new_line:
                    drawing_points.append([(center_x, center_y), (center_x, center_y), current_drawing_color])
                    start_new_line = False
                else:
                    drawing_points.append([drawing_points[-1][1], (center_x, center_y), current_drawing_color])

    for i in range(len(drawing_points)):
        start_point = drawing_points[i][0]
        end_point = drawing_points[i][1]
        cv2.line(frame, start_point, end_point, drawing_points[i][2], 3)

    cv2.imshow("Black?", frame)
    cv2.imshow("Test", mask)

    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        break
    elif key == ord("r"):
        drawing_points.clear()
    elif key == ord(" "):
        capture_points = not capture_points
        if capture_points == True:
            start_new_line = True

cap.release()