import tensorflow as tf
import numpy as np
import cv2
from sklearn.cluster import KMeans
from tensorflow.keras.preprocessing import image
import os

# Load trained model
model = tf.keras.models.load_model("models/closetcoach_cnn.h5")

# Class labels (same as training)
class_names = ['pants', 'shirt', 'shoes']

IMG_SIZE = 224

def extract_colors(img_path, k=3):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (64, 64))
    img = img.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(img)

    return kmeans.cluster_centers_.astype(int)

def predict_image_with_color(img_path):
    if not os.path.exists(img_path):
        raise FileNotFoundError("Image not found")

    # ----- Prediction -----
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]

    # ----- Color Extraction -----
    colors = extract_colors(img_path)

    return predicted_class, colors


# -------- TEST IMAGE --------
test_image_path =  "data/deepfashion/test/images/pants/img2.jpg"
 # change if needed

label, dominant_colors = predict_image_with_color(test_image_path)

print("Predicted clothing type:", label)
print("Dominant colors (RGB):", dominant_colors)


TEST_DIR = "data/deepfashion/test/images"

# pick first image automatically
for root, dirs, files in os.walk(TEST_DIR):
    if files:
        test_image_path = os.path.join(root, files[0])
        break

print("Using image:", test_image_path)
