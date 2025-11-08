import time
from model import model_fct
from detect_db import detect_fct
from eval import eval

if __name__ == "__main__":
    print("🚀 Démarrage du projet YOLOv8 - Détection de véhicules")

    # 1️⃣ Liste des modèles à gérer
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

    # 2️⃣ Téléchargement des nouveaux modèles
    t1 = time.time()
    models = model_fct(models_list)  # renvoie uniquement les nouveaux téléchargés
    t2 = time.time()
    print(f"⏱️ Durée du téléchargement des modèles : {t2 - t1:.2f} secondes")

    # 3️⃣ Détection si de nouveaux modèles ont été téléchargés
    if models:
        t3 = time.time()
        detect_fct(models)
        t4 = time.time()
        print(f"🔍 Durée du processus de détection : {t4 - t3:.2f} secondes")
    else:
        print("⚠️ Aucun nouveau modèle à détecter cette fois-ci.")

    # 4️⃣ Évaluation globale (peut comparer tous les modèles disponibles)
    t5 = time.time()
    eval()
    t6 = time.time()
    print(f"📊 Durée de l’évaluation des modèles : {t6 - t5:.2f} secondes")

    print("✅ Exécution terminée avec succès.")
