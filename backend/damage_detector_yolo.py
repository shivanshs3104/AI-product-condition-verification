from ultralytics import YOLO
import torch
from ultralytics.nn.tasks import DetectionModel

# allow YOLO DetectionModel in PyTorch safe loader
torch.serialization.add_safe_globals([DetectionModel])

# load pretrained YOLO model
model = YOLO("yolov8n.pt")

def detect_damage(image_path):

    results = model(image_path)

    detections = []
    severity_score = 0

    for r in results:
        boxes = r.boxes
        if boxes is None:
            continue

        for box in boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])

            label = model.names[cls_id]

            detections.append({
                "label": label,
                "confidence": round(confidence, 2)
            })

            severity_score += confidence * 2

    severity_score = min(int(severity_score), 10)

    if severity_score <= 2:
        damage_type = "No significant damage detected"
    elif severity_score <= 5:
        damage_type = "Minor damage detected"
    elif severity_score <= 8:
        damage_type = "Moderate damage detected"
    else:
        damage_type = "Severe damage detected"

    explanation = f"{damage_type}. Severity score: {severity_score}/10."

    return damage_type, severity_score, explanation, detections