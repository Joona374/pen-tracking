import cv2

cap = cv2.VideoCapture(1)  # Try 0, 1, 2... but 1 seems to be yours

#Check the capture device resolution
if not cap.isOpened():
    print("Error: Could not open video device")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    cropped_frame = frame[0:710, 380:870]
    if not ret:
        print("Failed to read frame")
        break
    cv2.imshow("DroidCam via USB", cropped_frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
