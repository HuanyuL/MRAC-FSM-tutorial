import cv2
import numpy as np
import socket
import time
import mediapipe as mp

from fsm_logic import FSM
from vision_utils import find_colored_circle, find_hand_center_mediapipe, detect_event

# === CONFIG ===
UDP_IP = "127.0.0.1"
UDP_PORT_GH = 5005
SEND_RATE = 0.1  # seconds

# === SETUP SOCKET ===
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# === FSM INSTANCE ===
fsm = FSM()

# === MEDIAPIPE HAND TRACKING SETUP ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mp_draw = mp.solutions.drawing_utils

# === HSV RANGE FOR DETECTION ===
hsv_lower = np.array([136, 54, 98])  # Lower hue to cover more purples/pinks
hsv_upper = np.array([255, 255, 255])  # Max out the range


# === TIMER VARIABLES ===
state_start_time = time.time()
previous_state = fsm.get_state()

# === HAND HISTORY FOR CIRCULAR GESTURE ===
hand_history = []

# === MAIN LOOP ===
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
last_sent = time.time()

print("[INFO] Starting FSM loop with MediaPipe...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, -1)
    frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    # Detect the event based on frame and current FSM state
    current_state = fsm.get_state()
    event = detect_event(frame, result, hsv_lower, hsv_upper, current_state, hand_history)

    if event:
        print(f"[EVENT] {event}")
        fsm.transition(event)

    # Update FSM state timer
    new_state = fsm.get_state()
    if new_state != previous_state:
        state_start_time = time.time()
        previous_state = new_state
        if new_state != "retry":
            hand_history.clear()

    # Fail condition for staying too long in challenge1
    if new_state == "challenge1" and (time.time() - state_start_time > 10):
        print("[EVENT] fail (timeout)")
        fsm.transition("fail")
        state_start_time = time.time()

    # Send FSM state to Grasshopper
    now = time.time()
    if now - last_sent > SEND_RATE:
        sock_send.sendto((fsm.get_state()).encode("utf-8"), (UDP_IP, UDP_PORT_GH))
        last_sent = now

    # === DEBUG VISUALS ===
    circle_pos, radius = find_colored_circle(frame, hsv_lower, hsv_upper)
    if circle_pos:
        cv2.circle(frame, circle_pos, radius, (0, 255, 0), 2)

    hand_pos = find_hand_center_mediapipe(frame, result)
    if hand_pos:
        cv2.circle(frame, hand_pos, 10, (255, 0, 0), -1)

    cv2.putText(
        frame, f"State: {fsm.get_state()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
    )

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("FSM + MediaPipe", frame)

    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
sock_send.close()
