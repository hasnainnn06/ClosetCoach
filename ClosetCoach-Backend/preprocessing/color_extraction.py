import cv2
import numpy as np
from sklearn.cluster import KMeans
import os

def extract_colors(image_path, k=3):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image could not be read. Check file format.")

    img = cv2.resize(img, (64, 64))
    img = img.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(img)

    colors = kmeans.cluster_centers_
    return colors.astype(int)


# -------- TEST WITH FIRST IMAGE IN FOLDER --------
if __name__ == "__main__":
    IMAGE_DIR = "data/deepfashion/processed_images"

    images = os.listdir(IMAGE_DIR)

    if len(images) == 0:
        raise ValueError("No images found in processed_images folder")

    test_image_path = os.path.join(IMAGE_DIR, images[0])

    colors = extract_colors(test_image_path)
    print("Dominant colors:", colors)
