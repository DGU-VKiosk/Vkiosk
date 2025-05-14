from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

yolo_model = YOLO("yolov8n.pt")

tracker = DeepSort(max_age=15)

def track_persons(frame):
    # Detect person using YOLO per frame
    results = yolo_model(frame, verbose=False)[0]
    detections = []

    # Check bound boxes of people
    for result in results.boxes:
        
        if yolo_model.names[int(result.cls[0])] == "person":
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            w, h = x2 - x1, y2 - y1
            conf = float(result.conf[0])

            if conf < 0.5:
                continue
            if w < 60 or h < 100:
                continue

            detections.append(([x1, y1, w, h], conf, 'person')) # For DeepSort
    tracks = tracker.update_tracks(detections, frame = frame) # Tracking

    person_boxes = []
    track_ids = []

    for track in tracks:    
        if not track.is_confirmed():
            continue
        x1, y1, x2, y2 = map(int, track.to_ltrb())
        person_boxes.append([x1, y1, x2, y2])
        track_ids.append(int(track.track_id))

    return person_boxes, track_ids