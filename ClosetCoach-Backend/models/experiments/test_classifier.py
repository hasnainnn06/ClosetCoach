import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

MODEL_PATH = "models/closetcoach_cnn.h5"
IMG_SIZE = 224

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Class names (from training folders)
CLASS_NAMES = sorted(os.listdir("data/deepfashion/train/images"))

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img, verbose=0)[0]

    top3_idx = np.argsort(preds)[-3:][::-1]
    top3 = [(CLASS_NAMES[i], preds[i]) for i in top3_idx]

    return top3


def test_folder(folder_path, samples=5):
    print(f"\n📂 Testing folder: {folder_path}")

    images = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    for img_name in images[:samples]:
        img_path = os.path.join(folder_path, img_name)
        preds = predict_image(img_path)

        print(f"\nImage: {img_name}")
        for cls, score in preds:
            print(f"  {cls:8s} → {score*100:.2f}%")


# -------- CHANGE CLASS TO TEST --------
TEST_CLASS = "top"  # change to pants, dress, skirt, shorts, jacket

test_folder(f"data/deepfashion/test/images/{TEST_CLASS}")
