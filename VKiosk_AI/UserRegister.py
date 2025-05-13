import cv2

def person_in_zone(x1, y1, x2, y2, zone):
    zx1, zy1, zx2, zy2 = zone
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    return zx1 <= cx <= zx2 and zy1 <= cy <= zy2

def check_user_registration(person_boxes, zone, current_id):
    if current_id is not None:
        return current_id
    for i, (x1, y1, x2, y2) in enumerate(person_boxes):
        if person_in_zone(x1, y1, x2, y2, zone):
            print("User registration completed")
            return i
    return None

def check_user_unregisteration(person_boxes, current_id): 
    if current_id is None:
        return None  
    
    if current_id >= len(person_boxes):
        print("User registration initialized")
        return None
    
    if cv2.waitKey(1) & 0xFF == ord('r'):
        print("User registration force initialized")
        return None
    
    return current_id
    

def draw_zone(frame, zone):
    x1, y1, x2, y2 = zone
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
    cv2.putText(frame, "Step Here", (x1 + 10, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
