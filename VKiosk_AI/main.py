from Camera import *
from PersonDetection import *
from HandTracking import *
from UserRegister import *
import cv2

# Initialize
zone = (440, 160, 880, 560) # Cognition Zone
cap = init_camera(0)        # Video Capture
registered_id = None        # Register ID

while True:
    frame = get_camera_frame(cap)   # Get camera frame
    boxes = detect_persons(frame)   # Get person boxes

    # Update registered id
    registered_id = check_user_registration(boxes, zone, registered_id)
    registered_id = check_user_unregisteration(boxes, registered_id)

    # Draw person box
    draw_person_boxes(frame, boxes, registered_id)

    # Draw cognition zone
    draw_zone(frame, zone)
    detect_and_draw_hands(frame, boxes, registered_id)

    # Display Camera
    cv2.imshow("Main", frame)

    # Exit Condition : Keycode.Q
    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break

cap.release()
cv2.destroyAllWindows()
