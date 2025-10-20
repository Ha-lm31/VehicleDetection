# train_yolo.py
from ultralytics import YOLO

# Charger le modèle pré-entraîné YOLOv8n
model = YOLO("yolov8n.pt")

# Lancer l'entraînement
model.train(
    data="data.yaml",   # notre fichier data
    epochs=2,          # nombre d'époques (ajuste selon ton dataset)
    imgsz=640,          # taille d’image
    batch=16,           # taille du lot
    name="yolov8n_custom"
)
