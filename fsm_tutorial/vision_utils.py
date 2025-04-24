import cv2
import numpy as np


def find_colored_circle(frame, hsv_lower, hsv_upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        if len(approx) > 5 and area > 100:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            return (int(x), int(y)), int(radius)
    return None, None


def find_hand_center_mediapipe(frame, results):
    if results.multi_hand_landmarks:
        h, w, _ = frame.shape
        for hand_landmarks in results.multi_hand_landmarks:
            wrist = hand_landmarks.landmark[0]
            cx, cy = int(wrist.x * w), int(wrist.y * h)
            return (cx, cy)
    return None


def is_thumbs_up(hand_landmarks):
    """
    Checks if the hand gesture corresponds to a thumbs up:
    - Thumb pointing up
    - All other fingers folded
    """
    if hand_landmarks:
        lm = hand_landmarks.landmark

        # Thumb
        is_thumb_up = lm[4].y < lm[3].y

        # Other fingers folded
        are_others_down = (
            lm[8].y > lm[6].y  # index
            and lm[12].y > lm[10].y  # middle
            and lm[16].y > lm[14].y  # ring
            and lm[20].y > lm[18].y  # pinky
        )

        return is_thumb_up and are_others_down
    return False


def detect_event(frame, results, hsv_lower, hsv_upper, current_state, hand_history):
    circle_pos, radius = find_colored_circle(frame, hsv_lower, hsv_upper)
    hand_pos = find_hand_center_mediapipe(frame, results)

    # Thumbs up only allowed when waiting to start
    if current_state == "start":
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if is_thumbs_up(hand_landmarks):
                    return "game_start"

    # Circular motion only allowed during challenge
    if current_state == "retry":
        if hand_pos:
            hand_history.append(hand_pos)
            if len(hand_history) > 20:
                hand_history.pop(0)

            if len(hand_history) >= 10:
                (cx, cy), r = cv2.minEnclosingCircle(np.array(hand_history))
                avg_dist = np.mean(
                    [np.sqrt((x - cx) ** 2 + (y - cy) ** 2) for (x, y) in hand_history]
                )
                max_dev = max(
                    [
                        abs(np.sqrt((x - cx) ** 2 + (y - cy) ** 2) - avg_dist)
                        for (x, y) in hand_history
                    ]
                )
                if max_dev < 30:
                    hand_history.clear()
                    return "retry_challenge1"

    # Bubble touch detection (available in many states if needed)
    if current_state in ["challenge1", "challenge2"]:
        if circle_pos and hand_pos:
            dx = hand_pos[0] - circle_pos[0]
            dy = hand_pos[1] - circle_pos[1]
            dist_sq = dx * dx + dy * dy
            if dist_sq < radius * radius:
                return "hand_over_bubble"

    return None
