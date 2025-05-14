from ultralytics import YOLO
import cv2

yolo_model = YOLO("yolov8n.pt")

def detect_persons(frame):
    # Detect person using YOLO per frame
    results = yolo_model(frame, verbose=False)[0]
    boxes = []

    # Check bound boxes of people
    for r in results.boxes:
        if yolo_model.names[int(r.cls[0])] == "person":
            boxes.append(list(map(int, r.xyxy[0])))
    return boxes

def draw_person_boxes(frame, boxes, registered_id, track_ids):
    for i, (x1, y1, x2, y2) in enumerate(boxes):
        tid = track_ids[i]
        color = (0, 255, 0) if tid == registered_id else (0, 0, 255)
        label = f"User {i}" if tid == registered_id else f"Person {i}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
