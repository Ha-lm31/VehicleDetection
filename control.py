import cv2, os

images_dir = "Images"
labels_dir = "Labels"

sample = os.listdir(images_dir)[:10]
for imgf in sample:
    img = cv2.imread(os.path.join(images_dir, imgf))
    h, w = img.shape[:2]
    name = os.path.splitext(imgf)[0]
    lbl = os.path.join(labels_dir, name + ".txt")
    if not os.path.exists(lbl): continue
    with open(lbl) as f:
        for line in f:
            parts = line.split()
            if len(parts) != 5: continue
            cls, xc, yc, ww, hh = parts
            xc = float(xc)*w; yc = float(yc)*h; ww = float(ww)*w; hh = float(hh)*h
            x1 = int(xc - ww/2); y1 = int(yc - hh/2)
            x2 = int(xc + ww/2); y2 = int(yc + hh/2)
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(img, cls, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    cv2.imshow("check", img)
    cv2.waitKey(0)
cv2.destroyAllWindows()
