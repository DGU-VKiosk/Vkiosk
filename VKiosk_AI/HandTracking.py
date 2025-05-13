import mediapipe as mp
import cv2
import pyautogui
from HandGesture import *

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

prev_positions = {}

screen_w, screen_h = pyautogui.size()

def hand_inside_box(x, y, box):
    x1, y1, x2, y2 = box
    return x1 <= x <= x2 and y1 <= y <= y2

def detect_and_draw_hands(frame, person_boxes, registered_id):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[i].classification[0].label
            if handedness != "Right":
                continue  # Ignore left hand

            wrist = hand_landmarks.landmark[0]                  # Get wrist
            h, w, _ = frame.shape                               # Get frame shape
            hand_x, hand_y = int(wrist.x * w), int(wrist.y * h) # Coordinate transformation

            matched_id = None                                   # Init matched id
            for j, box in enumerate(person_boxes):              # Check all person box and link hand
                if hand_inside_box(hand_x, hand_y, box):        
                    matched_id = j                           
                    break
            
            # Check registered person
            if matched_id == registered_id:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                print(f"Detected Hand {i}: {handedness} / wrist.x = {hand_x}")
                key = f"hand_{matched_id}"
                if key in prev_positions:
                    dy = prev_positions[key][1] - hand_y  # 위로 움직이면 dy > 0

                    if is_fist(hand_landmarks.landmark):
                        cv2.putText(frame, "Fist", (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
                    elif is_swip(prev_positions[key][0], hand_x, hand_landmarks.landmark) == "right":
                        direction = "Right Swipe"
                        cv2.putText(frame, direction, (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 0), 2)

                    elif is_swip(prev_positions[key][0], hand_x, hand_landmarks.landmark) == "left":
                        direction = "Left Swipe"
                        cv2.putText(frame, direction, (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 0), 2)    
                        
                    else :
                        cv2.putText(frame, "Default", (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 0), 2)  
                    

                prev_positions[key] = (hand_x, hand_y)
                cv2.putText(frame, "Registered User Hand", (hand_x, hand_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Move Cursor
                screen_x = int(wrist.x * screen_w)
                screen_y = int(wrist.y * screen_h)
                pyautogui.moveTo(screen_x, screen_y, duration=0.05)
