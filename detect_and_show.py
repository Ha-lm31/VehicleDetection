# detect_and_show.py
from ultralytics import YOLO
import cv2

# Charger le modèle entraîné
model = YOLO("runs/detect/train/weights/best.pt")

# Image à tester
img_path = "dataset/images/val/frame_0003_jpg.rf.7c2116971d2c01aa6a2c7d287dc7353f.jpg"  # remplace par ton image

# Exécuter la prédiction
results = model.predict(source=img_path, conf=0.4, save=False)

# Prendre la première sortie
r = results[0]
img = cv2.imread(img_path)

# Dessiner les boîtes sur l’image
for box in r.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
    cls = int(box.cls[0])
    conf = float(box.conf[0])
    label = f"{model.names[cls]} {conf:.2f}"
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img, label, (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# Enregistrer le résultat dans un fichier (car on ne peut pas afficher avec imshow)
output_path = "result_image.jpg"
cv2.imwrite(output_path, img)

print(f"✅ Image sauvegardée : {output_path}")
