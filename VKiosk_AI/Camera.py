import cv2

def init_camera(cam, width=1280, height=720):
    cap = cv2.VideoCapture(cam)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

def get_camera_frame(cap):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        raise RuntimeError("Camera disconnected")
    return frame