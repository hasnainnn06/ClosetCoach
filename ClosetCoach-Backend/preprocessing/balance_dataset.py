import os
import random
import shutil

BASE_DIR = "data/deepfashion/train/images"
TARGET_COUNT = 5000

for cls in os.listdir(BASE_DIR):
    cls_path = os.path.join(BASE_DIR, cls)
    images = os.listdir(cls_path)

    if len(images) <= TARGET_COUNT:
        continue

    random.shuffle(images)
    remove_imgs = images[TARGET_COUNT:]

    for img in remove_imgs:
        os.remove(os.path.join(cls_path, img))

    print(f"{cls} balanced to {TARGET_COUNT} images")
