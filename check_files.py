# check_files.py
## pour repérer images sans labels ou labels sans images.
import os

images_dir = "Images"
labels_dir = "Labels"

img_exts = {".jpg", ".jpeg", ".png"}
images = {os.path.splitext(f)[0]: f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in img_exts}
labels = {os.path.splitext(f)[0]: f for f in os.listdir(labels_dir) if f.endswith(".txt")}

only_images = sorted(set(images) - set(labels))
only_labels = sorted(set(labels) - set(images))

print(f"Images: {len(images)}, Labels: {len(labels)}")
print("Images sans label:", only_images[:10])
print("Labels sans image:", only_labels[:10])

# Optionnel : lister quelques exemples complets
pairs = sorted(set(images) & set(labels))
print("Exemples (image, label):", pairs[:5])
