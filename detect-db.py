# detect_db.py
# Exécute la détection pour chaque modèle sur le dossier Images/
# Sauvegarde un JSON par modèle dans /workspaces/model-V8/resultats
import os
import json
from tqdm import tqdm
import numpy as np

RESULTS_DIR = "/workspaces/model-V8/resultats"
IMAGES_DIR = "/workspaces/model-V8/Images"
VALID_CLASSES = ["car", "truck", "bus", "rickshaw", "bicycle"]

def _ensure_dirs():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

def _sorted_images_list():
    # retourne la liste d'images triées (important pour la heuristique "venant vers la caméra")
    exts = (".jpg", ".jpeg", ".png", ".bmp")
    files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(exts)]
    files.sort()  # suppose les noms contiennent un index (frame_0000_...)
    return [os.path.join(IMAGES_DIR, f) for f in files]

def _bbox_area(box):
    # box = [x1,y1,x2,y2]
    w = max(0, box[2] - box[0])
    h = max(0, box[3] - box[1])
    return w * h

def _iou(boxA, boxB):
    # bbox format [x1,y1,x2,y2]
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interW = max(0, xB - xA)
    interH = max(0, yB - yA)
    inter = interW * interH
    boxAA = max(0, (boxA[2]-boxA[0])*(boxA[3]-boxA[1]))
    boxBB = max(0, (boxB[2]-boxB[0])*(boxB[3]-boxB[1]))
    union = boxAA + boxBB - inter
    if union == 0:
        return 0.0
    return inter / union

def detect_fct(models):
    """
    models: liste de chemins vers les .pt
    Pour chaque modèle :
      - charge le modèle (ultralytics YOLO)
      - prédire sur chaque image
      - heuristique de tracking simple entre frames pour décider si un objet "vient vers la caméra"
      - sauvegarde JSON: liste d'entrées par image with counts
    """
    _ensure_dirs()

    # import ultralytics ici
    try:
        from ultralytics import YOLO
    except Exception as e:
        print("ERREUR : la librairie 'ultralytics' n'est pas installée. Installe-la : pip install ultralytics")
        raise e

    images = _sorted_images_list()
    if not images:
        print(f"Aucune image trouvée dans {IMAGES_DIR}. Place tes images (ex: frame_0000_*.jpg).")
        return

    for model_path in models:
        model_name = os.path.basename(model_path)
        out_json = os.path.join(RESULTS_DIR, model_name.replace(".pt", ".json"))
        print(f"--- Traitement du modèle {model_name} ---")
        try:
            yolo = YOLO(model_path)
        except Exception as e:
            print(f"Impossible de charger {model_path} : {e}")
            continue

        # stockage des detections par frame: list of dicts {'image':filename, 'boxes': [[x1,y1,x2,y2],...], 'classes': [name,...]}
        frames_det = []

        # prédiction : on utilisera la méthode predict pour chaque image pour obtenir bbox/class
        for img_path in tqdm(images, desc=f"predict {model_name}"):
            try:
                results = yolo.predict(source=img_path, imgsz=640, conf=0.25, verbose=False)  # results est une list-like
            except Exception as e:
                print(f"Erreur prédiction sur {img_path} : {e}")
                results = []

            # ultralytics retourne une liste d'objets Results (one per image)
            boxes = []
            classes = []
            if results:
                r = results[0]
                # r.boxes.xyxy, r.boxes.conf, r.boxes.cls
                try:
                    xyxy = r.boxes.xyxy.cpu().numpy() if hasattr(r.boxes, "xyxy") else np.array([])
                    cls = r.boxes.cls.cpu().numpy() if hasattr(r.boxes, "cls") else np.array([])
                except Exception:
                    # fallback si structure différente
                    try:
                        # r.boxes.data ? on essaye d'extraire
                        xyxy = np.array([b.xyxy for b in r.boxes]) if hasattr(r.boxes, "__iter__") else np.array([])
                        cls = np.array([b.cls for b in r.boxes]) if hasattr(r.boxes, "__iter__") else np.array([])
                    except Exception:
                        xyxy = np.array([])
                        cls = np.array([])

                for i, box in enumerate(xyxy):
                    try:
                        class_idx = int(cls[i])
                        class_name = r.names[class_idx] if hasattr(r, "names") else str(class_idx)
                        if class_name in VALID_CLASSES:
                            boxes.append([float(box[0]), float(box[1]), float(box[2]), float(box[3])])
                            classes.append(class_name)
                    except Exception:
                        continue

            frames_det.append({"image": os.path.basename(img_path), "boxes": boxes, "classes": classes})

        # Heuristique simple de tracking entre frames:
        # pour chaque detection de frame t, on cherche une detection similaire (IoU>0.3) dans t+1,
        # on suit la même détection et regarde si l'aire du bbox augmente => "approche"
        per_image_counts = []
        # Initialiser tracks: pour la frame 0, chaque bbox devient un track id
        # tracks: list of dict {id, last_box, last_area}
        next_track_id = 0
        prev_tracks = []

        for idx, frame in enumerate(frames_det):
            imgname = frame["image"]
            boxes = frame["boxes"]
            classes = frame["classes"]
            counts = {k: 0 for k in VALID_CLASSES}
            counts["total"] = 0

            # On essaie de mettre à jour prev_tracks vers current detections
            curr_tracks = []
            matched = set()
            for b_idx, box in enumerate(boxes):
                area = _bbox_area(box)
                cls = classes[b_idx]

                # chercher meilleur match dans prev_tracks
                best_tid = None
                best_iou = 0.0
                best_prev = None
                for t in prev_tracks:
                    i = _iou(box, t["last_box"])
                    if i > best_iou:
                        best_iou = i
                        best_prev = t
                        best_tid = t["id"]

                approaching = False
                # si on a un match raisonnable, comparer aire
                if best_iou >= 0.25 and best_prev is not None:
                    prev_area = best_prev["last_area"]
                    # si la taille augmente de plus de 8% -> on considère approche
                    if area > prev_area * 1.08:
                        approaching = True
                else:
                    # pas de track précédent : impossible de savoir -> on applique un seuil conservateur sur taille absolue?
                    # Ici on choisit d'ignorer l'incertitude et **compter uniquement si bbox est relativement grand** (heuristique)
                    # Cela réduit faux-positifs sur très petites detections
                    if area > 500:  # seuil arbitraire (tu peux ajuster)
                        approaching = True

                if approaching:
                    counts[cls] += 1
                    counts["total"] += 1

                # créer ou mettre à jour un track
                if best_tid is not None and best_iou >= 0.25:
                    # mettre à jour le track
                    curr_tracks.append({"id": best_tid, "last_box": box, "last_area": area})
                else:
                    # nouveau track
                    curr_tracks.append({"id": next_track_id, "last_box": box, "last_area": area})
                    next_track_id += 1

            # préparer pour image suivante
            prev_tracks = curr_tracks
            # enregistre les comptes
            per_image_counts.append({
                "id_images": imgname,
                "car": str(counts["car"]),
                "truck": str(counts["truck"]),
                "bus": str(counts["bus"]),
                "rickshaw": str(counts["rickshaw"]),
                "bicycle": str(counts["bicycle"]),
                "total": str(counts["total"])
            })

        # écriture JSON
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(per_image_counts, f, ensure_ascii=False, indent=2)
        print(f"Résultats écrits dans {out_json}")
