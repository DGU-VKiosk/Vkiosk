import mediapipe as mp
import cv2
import pyautogui
from HandGesture import *

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

prev_positions = {}

screen_w, screen_h = pyautogui.size()

swiping = False;
dragging = False;

def hand_inside_box(x, y, box):
    x1, y1, x2, y2 = box
    return x1 <= x <= x2 and y1 <= y <= y2

def detect_and_draw_hands(frame, person_boxes, registered_id):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    global swiping
    global dragging

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
                key = f"hand_{matched_id}"

                screen_x = int(wrist.x * screen_w)
                screen_y = int(wrist.y * screen_h)

                if key in prev_positions:
                    prev_x, prev_y = prev_positions[key]

                    if is_fist(hand_landmarks.landmark):
                        if not dragging:
                            pyautogui.mouseDown(screen_x, screen_y)
                            dragging = True
                        cv2.putText(frame, "Fist", (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
                    elif is_swip(prev_x, hand_x, hand_landmarks.landmark) == "right":
                        direction = "Right Swipe"
                        if swiping == False:
                            swiping = True
                        cv2.putText(frame, direction, (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 0, 0), 2)

                    elif is_swip(prev_x, hand_x, hand_landmarks.landmark) == "left":
                        direction = "Left Swipe"
                        if swiping == False:
                            swiping = True
                        cv2.putText(frame, direction, (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 0, 0), 2)    
                        
                    elif is_click(prev_y, hand_y, hand_landmarks.landmark):
                        pyautogui.click()   # Click
                        cv2.putText(frame, "Click", (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 200), 2)   
                        
                    else :
                        if dragging:
                            pyautogui.mouseUp(screen_x, screen_y)
                            dragging = False
                        cv2.putText(frame, "Default", (hand_x, hand_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 150, 0), 2)  
                    
                pyautogui.moveTo(screen_x, screen_y, duration=0.05)

                prev_positions[key] = (hand_x, hand_y)
                cv2.putText(frame, "Registered User Hand", (hand_x, hand_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
