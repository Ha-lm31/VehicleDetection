# Exécution
 1. check_files.py
 2. prepare_dataset_split.py
 3. train_yolo.py

# cmd

```
pip install --upgrade pip
pip install ultralytics

sudo apt-get update && sudo apt-get install -y libgl1

yolo detect train model=yolov8n.pt data=data.yaml epochs=2 imgsz=640

yolo detect predict model=/workspaces/model-V8/runs/detect/train/weights/best.pt source=/workspaces/model-V8/dataset/images/val/ save=True

yolo detect predict model=/workspaces/model-V8/runs/detect/train/weights/best.pt source=/workspaces/model-V8/test_image/ save=True
```


```
yolo detect train model=/workspaces/model-V8/runs/detect/train/weights/best.pt data=data.yaml epochs=50 imgsz=640

```