import cv2
import numpy as np
import mss

cap_region = {"top": 110, "left": 0, "width": 940, "height": 830}

with mss.mss() as sct:
    while True:
        screenshot = sct.grab(cap_region)
        img = np.array(screenshot)
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_green = np.array((35, 60, 60))
        upper_green = np.array((80, 255, 255))

        mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask_copy = cv2.cvtColor(mask.copy(), cv2.COLOR_GRAY2BGR)
        

        cv2.drawContours(mask_copy, contours, 0, (0, 0, 255), 5)

        cv2.imshow("Test", frame)
        cv2.imshow("Mask", mask_copy)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

