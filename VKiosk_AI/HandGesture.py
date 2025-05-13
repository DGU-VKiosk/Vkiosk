TAP_THRESHOLD = 15
SWIPE_THRESHOLD = 100

def is_fist(landmarks):
    tips = [8, 12, 16, 20]
    return sum(landmarks[tip].y > landmarks[tip - 2].y for tip in tips) >= 4

def is_swip(pre_x, cur_x, landmarks):
    tips = [8, 12, 16, 20]
    folded_finger = sum(landmarks[tip].y > landmarks[tip - 2].y for tip in tips)
    
    if folded_finger == 0:
        dx = cur_x - pre_x
        if abs(dx) > SWIPE_THRESHOLD:
            if dx > 0:
                return "left"
            elif dx < 0:
                return "right"