from ultralytics import YOLO
model = YOLO("runs/detect/train/weights/best.pt")
metrics = model.val(data="data.yaml", batch=16, imgsz=640)
print(metrics.box.map0_5)  # mAP@0.5
