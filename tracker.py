import cv2
import numpy as np
import mss

cap_region = {"top": 110, "left": 0, "width": 940, "height": 830}
drawing_points = []
current_drawing_color = (0, 0, 255)
capture_points = False
start_new_line = True

with mss.mss() as sct:
    while True:
        screenshot = sct.grab(cap_region)
        img = np.array(screenshot)
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 70, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 70, 50])
        upper_red2 = np.array([180, 255, 255])
        red_mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        red_mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        lower_green = np.array((35, 60, 60))
        upper_green = np.array((80, 255, 255))
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        lower_blue = np.array((100, 60, 60))
        upper_blue = np.array((130, 255, 255))
        blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

        green_count = cv2.countNonZero(green_mask)
        blue_count = cv2.countNonZero(blue_mask)
        red_count = cv2.countNonZero(red_mask)

        mask_to_use = red_mask

        if max(green_count, blue_count, red_count) < 50:
            current_drawing_color = (255, 255, 255)
        elif green_count > blue_count and green_count > red_count:
            current_color = "green"
            mask_to_use = green_mask
            current_drawing_color = (0, 255, 0)

        elif blue_count > red_count:
            current_color = "blue"
            mask_to_use = blue_mask
            current_drawing_color = (255, 0, 0)

        else:
            current_color = "red"
            mask_to_use = red_mask
            current_drawing_color = (0, 0, 255)


        contours, hierarchy = cv2.findContours(mask_to_use, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if capture_points:
            if contours:
                biggest = max(contours, key=cv2.contourArea)
                M = cv2.moments(biggest)
                if M["m00"]:
                    center_x = int(M["m10"]/M["m00"])
                    center_y = int(M["m01"]/M["m00"])
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 0), -1)
                    draw_with_color = current_drawing_color
                    if start_new_line:
                        drawing_points.append([(center_x, center_y), (center_x, center_y), draw_with_color])
                        start_new_line = False
                    else:
                        drawing_points.append([drawing_points[-1][1], (center_x, center_y), draw_with_color])



        trail_canvas = np.zeros((screenshot.height, screenshot.width, 3), dtype=np.uint8)
        for i in range(len(drawing_points)):
            start_point = drawing_points[i][0]
            end_point = drawing_points[i][1]
            cv2.line(frame, start_point, end_point, drawing_points[i][2], 3)

        cv2.imshow("Black?", trail_canvas)

        # mask_copy = cv2.cvtColor(mask.copy(), cv2.COLOR_GRAY2BGR)
        # cv2.drawContours(mask_copy, contours, 0, (0, 0, 255), 5)
        # cv2.imshow("Mask", mask_copy)

        cv2.imshow("Test", frame)
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
        
