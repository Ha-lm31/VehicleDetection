# main.py
# Orchestration principale

from model import model_fct
from detect_db import detect_fct
from eval import eval as run_eval
import os

if __name__ == "__main__":
    # Liste initiale des modèles (nom de fichier attendu, ex: 'yolov8n.pt')
    models_list = [
        "yolov8n.pt",
        "yolov8m.pt",
        "yolov8s.pt"
        # ajoute d'autres modèles si tu veux
    ]

    print("==> Initialisation / vérification des modèles ...")
    models = model_fct(models_list)  # retourne la liste des modèles trouvés (chemins complets)

    if not models:
        print("Aucun modèle disponible dans le dossier models/. Place manuellement les .pt ou vérifie la connexion.")
    else:
        print(f"Modèles disponibles : {len(models)}")
        print("==> Lancement de la détection pour chaque modèle ...")
        detect_fct(models)

        print("==> Évaluation des modèles ...")
        run_eval()

    print("Terminé.")
