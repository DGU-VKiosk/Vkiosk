from Camera import *
from PersonDetection import draw_person_boxes
from HandTracking import detect_and_draw_hands
from UserRegister import user_registration, user_unregisteration, draw_zone
from Tracker import track_persons
import cv2

# Initialize
zone = (440, 160, 880, 560) # Cognition Zone
cap = init_camera(0)        # Video Capture
registered_id = None        # Register ID
registered_box = None

while True:
    frame = get_camera_frame(cap)   # Get camera frame
    #boxes = detect_persons(frame)   # Get person boxes

    boxes, track_ids = track_persons(frame)

    # Update registered id
    if registered_id == None:
        # Draw cognition zone
        draw_zone(frame, zone)
        registered_id = user_registration(boxes, zone, registered_id, track_ids)
    else:
        registered_id = user_unregisteration(registered_id, track_ids)
        # Detect and Draw hands
        detect_and_draw_hands(frame, boxes, registered_id, track_ids)

    # Draw person box
    draw_person_boxes(frame, boxes, registered_id, track_ids)

    # Display Camera
    cv2.imshow("Main", frame)

    # Exit Condition : Keycode.Q
    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break

cap.release()
cv2.destroyAllWindows()
