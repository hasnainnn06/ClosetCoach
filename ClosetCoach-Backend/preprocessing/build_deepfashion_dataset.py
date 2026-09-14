import os
import shutil
import random

SOURCE_ROOT = r"data/deepfashion/img_highres"
TARGET_ROOT = "data/deepfashion"
TRAIN_RATIO = 0.8

CATEGORY_MAP = {
    "top": [
        "MEN/Shirts_Polos",
        "MEN/Tees_Tanks",
        "WOMEN/Blouses_Shirts",
        "WOMEN/Graphic_Tees",
        "WOMEN/Tees_Tanks"
    ],
    "pants": [
        "MEN/Pants",
        "MEN/Denim",
        "WOMEN/Pants",
        "WOMEN/Denim",
        "WOMEN/Leggings"
    ],
    "dress": [
        "WOMEN/Dresses",
        "WOMEN/Rompers_Jumpsuits"
    ],
    "jacket": [
        "MEN/Jackets_Vests",
        "MEN/Sweaters",
        "MEN/Sweatshirts_Hoodies",
        "WOMEN/Jackets_Coats",
        "WOMEN/Cardigans",
        "WOMEN/Sweaters",
        "WOMEN/Sweatshirts_Hoodies"
    ],
    "skirt": [
        "WOMEN/Skirts"
    ],
    "shorts": [
        "MEN/Shorts",
        "WOMEN/Shorts"
    ],
    "suit": [
        "MEN/Suiting"
    ]
}

def collect_images_recursive(folder):
    image_paths = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                image_paths.append(os.path.join(root, f))
    return image_paths

def split_and_copy(images, train_dst, test_dst):
    random.shuffle(images)
    split = int(len(images) * TRAIN_RATIO)

    for img in images[:split]:
        shutil.copy(img, train_dst)

    for img in images[split:]:
        shutil.copy(img, test_dst)

for category, folders in CATEGORY_MAP.items():
    train_out = os.path.join(TARGET_ROOT, "train/images", category)
    test_out = os.path.join(TARGET_ROOT, "test/images", category)

    os.makedirs(train_out, exist_ok=True)
    os.makedirs(test_out, exist_ok=True)

    all_images = []

    for folder in folders:
        src = os.path.join(SOURCE_ROOT, folder)
        if not os.path.exists(src):
            continue

        imgs = collect_images_recursive(src)
        print(f"{folder}: {len(imgs)} images found")
        all_images.extend(imgs)

    print(f"Total for {category}: {len(all_images)} images")

    if all_images:
        split_and_copy(all_images, train_out, test_out)

print("✅ DeepFashion dataset rebuilt successfully")
