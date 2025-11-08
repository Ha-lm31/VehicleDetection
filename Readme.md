# CMD

```
python --version
cd Images
cd models
cd resultats
cd ..

git status
git add .
git commit -m "1st commit"
git push -u origin main \ git push -u origin main --force


---
git rm --cached models/*.pt

echo "models/*.pt" >> .gitignore

git add .gitignore
git commit -am "Ignorer les fichiers modèles (.pt) pour GitHub Codespaces"
git push -u origin main --force

```

## main.py

1. initiler : models_list = ['yolov8n.pt', 'yolov8m.pt',.. ]
2. appelle la fonction : model_fct(models_list) -> models (list des modéles trouvé est telecharger)
3. appelle la fonction : detect-fct(models) 
4. appelle la fonction : eval() -> le meuiller models

## model.py

def model_fct(models): 
la fonction qui télécharger les models de la list dans le dossier "/workspaces/model-V8/models", s'il existe ne pas installé, met un fichier "models.txt" contient les list des modéls est leur type si installe met installer si erreur mes erreur.
et returne la liste des models dans le dossier.

## detect-db.py

def detect_fct(model):
appliquer les models du dossier "/workspaces/model-V8/models" sur les images du dossier "/workspaces/model-V8/Images", en détectant les déffirentes objet dans l'images ["car", "truck", "bus", "rickshaw", "bicycle"] à condition qui viens vers la caméra.
et enregistrer un fichier JSON a le meme nom du model 'yolov8n.pt' -> 'yolov8n.json' contient les informations suivantes 
"[{'id_images': "frame_0000_jpg.rf.02488de83e72f637bed5d2fdfc2cc10b.jpg",
'car':'3',
'truck':'1',
'bus':'2',
'rickshaw':'0',
'bicycle':'0',
'total':'6'},
{'id_images': "frame_0000_jpg.rf.02488de83e72f637bed5d2fdfc2cc1.jpg",
'car':'2',
'truck':'1',
'bus':'2',
'rickshaw':'0',
'bicycle':'0',
'total':'5'},..]" 
et enregistrer les fichier dans le dosssier "/workspaces/model-V8/resultats"

## eval.py

def eval():
cette fonction utilise les résultats du "/workspaces/model-V8/resultats", pour comparer entre les modeles et enregistrer dans un fichier un tableaux contient les models du plus haut au bas avec le nombre total de véhicules

# Code

## main.py

```
# main.py
# Orchestration principale

from model import model_fct
from detect_db import detect_fct
from eval import eval as run_eval
import os
import time

if __name__ == "__main__":
    # Liste initiale des modèles (nom de fichier attendu, ex: 'yolov8n.pt')
    models_list = [
        # YOLOv8
        "yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt",
        # YOLOv9
        "yolov9t.pt", "yolov9s.pt", "yolov9m.pt", "yolov9c.pt", "yolov9e.pt",
        # YOLOv10
        "yolov10n.pt", "yolov10s.pt", "yolov10m.pt", "yolov10b.pt", "yolov10l.pt", "yolov10x.pt",
        # YOLOv11
        "yolov11n.pt", "yolov11s.pt", "yolov11m.pt", "yolov11l.pt", "yolov11x.pt",
        # YOLOv12
        "yolov12n.pt", "yolov12s.pt", "yolov12m.pt", "yolov12l.pt", "yolov12x.pt"
    ]

    t1 = time.time()
    print("==> Initialisation / vérification des modèles ...")
    models = model_fct(models_list)  # retourne la liste des modèles trouvés (chemins complets)
    t2 = time.time()

    if not models:
        print("Aucun modèle disponible dans le dossier models/. Place manuellement les .pt ou vérifie la connexion.")
    else:
        print(f"Modèles disponibles : {len(models)}")
        t3 = time.time()
        print("==> Lancement de la détection pour chaque modèle ...")
        detect_fct(models)
        t4 = time.time()

        t5 = time.time()
        print("==> Évaluation des modèles ...")
        run_eval()
        t6 = time.time()

    print("Terminé.")

print(f"⏱️ Durée du téléchargement des modèles : {t2 - t1:.2f} secondes")
print(f"🔍 Durée du processus de détection : {t4 - t3:.2f} secondes")
print(f"📊 Durée de l’évaluation des modèles : {t6 - t5:.2f} secondes")

```

## model.py

```
# model.py
# Téléchargement et gestion des modèles YOLOv8
import os
import urllib.request
import traceback

MODELS_DIR = "/workspaces/model-V8/models"
MODELS_TXT = os.path.join("/workspaces/model-V8", "models.txt")

# Liens officiels Ultralytics YOLOv8 (HuggingFace)
YOLO_URLS = {
    "yolov8n.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt",
    "yolov8s.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt",
    "yolov8m.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt",
    "yolov8l.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt",
    "yolov8x.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt",
}


def _ensure_dirs():
    """Créer le dossier models s'il n'existe pas."""
    os.makedirs(MODELS_DIR, exist_ok=True)


def _write_models_txt(entries):
    """Écrit le fichier models.txt avec l'état d'installation."""
    with open(MODELS_TXT, "w", encoding="utf-8") as f:
        for name, status in entries.items():
            f.write(f"{name} : {status}\n")


def _download_file(url, dest):
    """Télécharge un fichier depuis une URL."""
    try:
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {url}: {e}")
        return False


def model_fct(models_list):
    """
    Télécharge les modèles YOLOv8 s'ils ne sont pas encore présents.
    - Les fichiers sont placés dans /workspaces/model-V8/models/
    - Un fichier models.txt est créé avec l'état (installé / erreur)
    - Retourne la liste complète des chemins de modèles disponibles
    """
    _ensure_dirs()
    status = {}
    found_models = []

    for model_name in models_list:
        model_path = os.path.join(MODELS_DIR, model_name)

        if os.path.isfile(model_path):
            status[model_name] = "✅ déjà installé"
            found_models.append(model_path)
            continue

        print(f"⬇️ Téléchargement du modèle {model_name} ...")

        # vérifier si on connaît l’URL
        url = YOLO_URLS.get(model_name)
        if url is None:
            status[model_name] = "⚠️ URL inconnue (ajoute-la manuellement)"
            print(f"URL manquante pour {model_name}.")
            continue

        try:
            ok = _download_file(url, model_path)
            if ok and os.path.isfile(model_path):
                status[model_name] = "✅ installé"
                found_models.append(model_path)
                print(f"✔️ {model_name} téléchargé avec succès.")
            else:
                status[model_name] = "❌ erreur téléchargement"
        except Exception:
            traceback.print_exc()
            status[model_name] = "❌ exception pendant le téléchargement"

    # Lister aussi les modèles déjà présents
    for fname in os.listdir(MODELS_DIR):
        if fname.endswith(".pt"):
            path = os.path.join(MODELS_DIR, fname)
            if path not in found_models:
                found_models.append(path)
                if fname not in status:
                    status[fname] = "✅ trouvé localement"

    # Écriture du fichier models.txt
    _write_models_txt(status)
    print(f"📝 État des modèles écrit dans {MODELS_TXT}")

    return found_models

```

```
import os
from ultralytics import YOLO
from tqdm import tqdm

def model_fct(models_list):
    """
    Télécharge automatiquement les modèles YOLOv8 spécifiés dans 'models_list'
    vers le dossier '/workspaces/model-V8/models'.
    - Ne retélécharge pas les modèles déjà présents.
    - Enregistre un log dans 'models/models.txt' avec le statut de chaque modèle.
    - Retourne la liste des nouveaux modèles téléchargés.
    """

    models_dir = "/workspaces/model-V8/models"
    os.makedirs(models_dir, exist_ok=True)

    log_path = os.path.join(models_dir, "models.txt")
    installed_models = []
    newly_downloaded = []

    # Charger la liste des modèles déjà installés à partir du fichier log
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                parts = line.strip().split(" - ")
                if len(parts) >= 2 and parts[1] == "installé":
                    installed_models.append(parts[0])

    # Télécharger uniquement les modèles absents
    with open(log_path, "a") as log_file:
        for model_name in tqdm(models_list, desc="📦 Téléchargement des modèles"):
            model_path = os.path.join(models_dir, model_name)

            try:
                if model_name not in installed_models and not os.path.exists(model_path):
                    print(f"⬇️ Téléchargement de {model_name} ...")
                    model = YOLO(model_name)  # télécharge automatiquement
                    model.save(model_path)
                    log_file.write(f"{model_name} - installé\n")
                    newly_downloaded.append(model_name)
                else:
                    log_file.write(f"{model_name} - déjà installé\n")

            except Exception as e:
                log_file.write(f"{model_name} - erreur: {str(e)}\n")
                print(f"❌ Erreur lors du téléchargement de {model_name}: {e}")

    print(f"\n✅ Téléchargement terminé. Nouveaux modèles : {newly_downloaded}")
    return newly_downloaded

```
## detect_db.py

```
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

```

## eval.py

```
# eval.py
# Lit tous les JSON dans resultats/ et produit un tableau trié des modèles par total véhicules détectés

import os
import json
import csv

RESULTS_DIR = "/workspaces/model-V8/resultats"
OUT_CSV = os.path.join("/workspaces/model-V8", "evaluation.csv")
OUT_JSON = os.path.join("/workspaces/model-V8", "evaluation.json")

def eval():
    files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".json")]
    if not files:
        print(f"Aucun fichier de résultats (.json) dans {RESULTS_DIR}. Lance d'abord detect_fct().")
        return

    summary = []
    for fname in files:
        fpath = os.path.join(RESULTS_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Impossible de lire {fpath} : {e}")
            continue

        total = 0
        for entry in data:
            try:
                total += int(entry.get("total", 0))
            except Exception:
                pass

        summary.append({"model": fname.replace(".json", ""), "total_vehicles": total})

    # tri décroissant
    summary.sort(key=lambda x: x["total_vehicles"], reverse=True)

    # écrire CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["rank", "model", "total_vehicles"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, s in enumerate(summary, 1):
            writer.writerow({"rank": i, "model": s["model"], "total_vehicles": s["total_vehicles"]})

    # écrire JSON
    with open(OUT_JSON, "w", encoding="utf-8") as jf:
        json.dump(summary, jf, ensure_ascii=False, indent=2)

    # affiche le tableau
    print("=== Résultats de l'évaluation (du meilleur au moins bon) ===")
    for i, s in enumerate(summary, 1):
        print(f"{i}. {s['model']}  —  total véhicules détectés : {s['total_vehicles']}")

    print(f"Fichiers écrits : {OUT_CSV}, {OUT_JSON}")

```