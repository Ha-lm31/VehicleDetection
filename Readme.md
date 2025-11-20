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

---
# Installer BFG Repo-Cleaner (outil rapide pour nettoyer l'historique)
sudo apt-get update && sudo apt-get install -y openjdk-17-jre-headless
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar -O bfg.jar

# Supprimer tous les fichiers .pt de l'historique Git
java -jar bfg.jar --delete-files *.pt

git reflog expire --expire=now --all && git gc --prune=now --aggressive

git push origin --force


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

