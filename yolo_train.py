from ultralytics import YOLO

# Create a new YOLO model from scratch
model = YOLO("yolov8n.yaml")

results = model.train(data="./config.yaml", epochs=120)
