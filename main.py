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
