import os
import shutil
from ultralytics import YOLO
from tqdm import tqdm

def model_fct(models_list):
    """
    Télécharge automatiquement les modèles YOLOv8 spécifiés dans 'models_list'
    dans le dossier '/workspaces/model-V8/models'.
    - Ne retélécharge pas les modèles déjà présents.
    - Enregistre un log dans 'models/models.txt' avec le statut de chaque modèle.
    - Supprime les copies inutiles dans la racine du projet.
    - Retourne la liste des nouveaux modèles téléchargés.
    """

    base_dir = "/workspaces/model-V8"
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    log_path = os.path.join(models_dir, "models.txt")
    installed_models = []
    newly_downloaded = []

    # Charger les modèles déjà installés
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                parts = line.strip().split(" - ")
                if len(parts) >= 2 and parts[1] == "installé":
                    installed_models.append(parts[0])

    with open(log_path, "a") as log_file:
        for model_name in tqdm(models_list, desc="📦 Téléchargement des modèles"):
            model_path = os.path.join(models_dir, model_name)

            try:
                # Si non installé
                if model_name not in installed_models and not os.path.exists(model_path):
                    print(f"⬇️ Téléchargement de {model_name} ...")
                    model = YOLO(model_name)  # Téléchargement automatique
                    # Déplacer le fichier téléchargé s’il est dans la racine
                    if os.path.exists(os.path.join(base_dir, model_name)):
                        shutil.move(
                            os.path.join(base_dir, model_name),
                            model_path
                        )
                    log_file.write(f"{model_name} - installé\n")
                    newly_downloaded.append(model_name)
                else:
                    log_file.write(f"{model_name} - déjà installé\n")

            except Exception as e:
                log_file.write(f"{model_name} - erreur: {str(e)}\n")
                print(f"❌ Erreur lors du téléchargement de {model_name}: {e}")

    print(f"\n✅ Téléchargement terminé. Nouveaux modèles : {newly_downloaded}")
    return newly_downloaded
