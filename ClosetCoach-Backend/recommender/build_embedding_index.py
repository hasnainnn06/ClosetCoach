import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

MODEL_PATH = "models/embedding_model.h5"
DATASET_ROOT = "data/deepfashion/visual"
OUTPUT_PATH = "recommender/embedding_index.pkl"
IMG_SIZE = 224

model = tf.keras.models.load_model(MODEL_PATH)

def extract_embedding(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    emb = model.predict(img, verbose=0)[0]
    return emb / np.linalg.norm(emb)

index = []

for gender in ["men", "women"]:
    gender_dir = os.path.join(DATASET_ROOT, gender)
    if not os.path.exists(gender_dir):
        continue

    for category in os.listdir(gender_dir):
        cat_dir = os.path.join(gender_dir, category)
        if not os.path.isdir(cat_dir):
            continue

        for img_name in os.listdir(cat_dir):
            if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            img_path = os.path.join(cat_dir, img_name)

            try:
                emb = extract_embedding(img_path)
                index.append({
                    "path": img_path,
                    "embedding": emb,
                    "gender": gender,
                    "category": category
                })
            except Exception as e:
                print("Skipping:", img_path)

with open(OUTPUT_PATH, "wb") as f:
    pickle.dump(index, f)

print(f"✅ Embedding index rebuilt with {len(index)} items")
