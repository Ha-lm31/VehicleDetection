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
