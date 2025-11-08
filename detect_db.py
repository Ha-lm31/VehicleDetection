import os
import json
from ultralytics import YOLO
from tqdm import tqdm

def detect_fct(models):
    """
    Applique chaque modèle YOLOv8 du dossier 'models/' sur les images du dossier 'Images/',
    détecte les objets ['car', 'truck', 'bus', 'rickshaw', 'bicycle'],
    et enregistre les résultats dans '/workspaces/model-V8/resultats/'.
    """

    models_dir = "/workspaces/model-V8/models"
    images_dir = "/workspaces/model-V8/Images"
    results_dir = "/workspaces/model-V8/resultats"
    os.makedirs(results_dir, exist_ok=True)

    # Vérifie la présence d’images
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not image_files:
        print("⚠️ Aucune image trouvée dans le dossier Images/.")
        return

    for model_name in models:
        model_path = os.path.join(models_dir, model_name)
        if not os.path.exists(model_path):
            print(f"❌ Modèle introuvable : {model_name}")
            continue

        print(f"\n🔍 Détection avec le modèle : {model_name}")
        model = YOLO(model_path)

        results_data = []

        # Parcourir les images avec barre de progression
        for img_file in tqdm(image_files, desc=f"Analyse ({model_name})"):
            img_path = os.path.join(images_dir, img_file)
            results = model(img_path, verbose=False)

            # Compter les objets détectés
            labels = ['car', 'truck', 'bus', 'rickshaw', 'bicycle']
            counts = {label: 0 for label in labels}

            for box in results[0].boxes:
                cls = int(box.cls[0])
                name = model.names.get(cls, "")
                if name in counts:
                    counts[name] += 1

            total = sum(counts.values())
            data = {
                "id_image": img_file,
                **counts,
                "total": total
            }
            results_data.append(data)

        # Sauvegarder en JSON
        json_path = os.path.join(results_dir, model_name.replace(".pt", ".json"))
        with open(json_path, "w") as f:
            json.dump(results_data, f, indent=4)

        print(f"✅ Résultats enregistrés dans : {json_path}")
