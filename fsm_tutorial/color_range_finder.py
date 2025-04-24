import cv2
import numpy as np


# Create a window with trackbars
def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 400, 300)

# Create trackbars for HSV range
cv2.createTrackbar("LH", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("UH", "Trackbars", 179, 255, nothing)
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)

# Capture image from camera
cap = cv2.VideoCapture(1)  # Change to 0 if using default camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Press SPACE to capture an image")

captured = False
frame = None

# Capture an image
while not captured:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, -1)  # Flip the frame vertically
    frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)  # Resize the frame

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC to exit
        break
    elif key == 32:  # SPACE to capture
        captured = True
        cap.release()
        cv2.destroyWindow("Camera")

# Start slider interface
while True:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get current positions of trackbars
    lh = cv2.getTrackbarPos("LH", "Trackbars")
    ls = cv2.getTrackbarPos("LS", "Trackbars")
    lv = cv2.getTrackbarPos("LV", "Trackbars")
    uh = cv2.getTrackbarPos("UH", "Trackbars")
    us = cv2.getTrackbarPos("US", "Trackbars")
    uv = cv2.getTrackbarPos("UV", "Trackbars")

    lower_hsv = np.array([lh, ls, lv])
    upper_hsv = np.array([uh, us, uv])

    # Create a mask and result image
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Filtered Color", result)

    key = cv2.waitKey(1)
    if key == 27:  # ESC to exit
        break

cv2.destroyAllWindows()
