import cv2
import numpy as np

IMG_SIZE = 224

def preprocess_for_inference(image_path):
    """
    Preprocess a single image for CNN / embedding inference.
    """
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Could not read image from path")

    # Convert BGR (OpenCV default) to RGB (TensorFlow expects RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)  # (1, 224, 224, 3)

    return img
