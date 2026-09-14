import cv2
import os
from tqdm import tqdm

INPUT_DIR = "data/deepfashion/images"
OUTPUT_DIR = "data/deepfashion/processed_images"

IMG_SIZE = 224

os.makedirs(OUTPUT_DIR, exist_ok=True)

for img_name in tqdm(os.listdir(INPUT_DIR)):
    img_path = os.path.join(INPUT_DIR, img_name)

    img = cv2.imread(img_path)

    if img is None:
        continue

    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0   # make pixels between 0 and 1

    save_path = os.path.join(OUTPUT_DIR, img_name)
    cv2.imwrite(save_path, (img * 255).astype("uint8"))

print("Image preprocessing done!")
