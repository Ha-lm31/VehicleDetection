# prepare_dataset_split.py
## effectue le split 80/20 et crée la structure
'''
Après exécution tu auras :
dataset/images/train, dataset/images/val
dataset/labels/train, dataset/labels/val
'''

import os, random, shutil

random.seed(42)

base = "."  # modifie si besoin
images_dir = os.path.join(base, "Images")
labels_dir = os.path.join(base, "Labels")

out = os.path.join(base, "dataset")
images_out = os.path.join(out, "images")
labels_out = os.path.join(out, "labels")

for p in [images_out, labels_out]:
    for sub in ["train", "val"]:
        os.makedirs(os.path.join(p, sub), exist_ok=True)

# lister images (basename sans extension)
img_exts = {".jpg", ".jpeg", ".png"}
items = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in img_exts]
items.sort()
random.shuffle(items)

split = int(0.8 * len(items))
train = items[:split]
val = items[split:]

def copy_list(lst, subset):
    for img in lst:
        name = os.path.splitext(img)[0]
        src_img = os.path.join(images_dir, img)
        src_lbl = os.path.join(labels_dir, name + ".txt")
        dst_img = os.path.join(images_out, subset, img)
        dst_lbl = os.path.join(labels_out, subset, name + ".txt")
        shutil.copy2(src_img, dst_img)
        if os.path.exists(src_lbl):
            shutil.copy2(src_lbl, dst_lbl)
        else:
            # créer fichier vide si label manquant (prévenir erreurs)
            open(dst_lbl, "w").close()

copy_list(train, "train")
copy_list(val, "val")

print(f"Total images: {len(items)} | train: {len(train)} | val: {len(val)}")
print("Dataset ready in 'dataset/images' and 'dataset/labels'")
