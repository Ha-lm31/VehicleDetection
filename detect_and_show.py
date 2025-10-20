from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train/weights/best.pt")  # chemin vers ton best.pt
img_path = "dataset/images/val/some_image.jpg"      # exemple
res = model.predict(source=img_path, conf=0.4, save=False)

# res est une liste, on prend res[0]
r = res[0]
# dessiner avec OpenCV
img = cv2.imread(img_path)
for box in r.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
    cls = int(box.cls[0])
    conf = float(box.conf[0])
    label = f"{model.names[cls]} {conf:.2f}"
    cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
    cv2.putText(img, label, (x1, max(15,y1-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

cv2.imshow("res", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
