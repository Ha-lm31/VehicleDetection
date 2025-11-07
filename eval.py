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
