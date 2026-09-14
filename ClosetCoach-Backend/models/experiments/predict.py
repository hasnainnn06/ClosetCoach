import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

# Load model
model = tf.keras.models.load_model("models/closetcoach_cnn.h5")

# Class labels (must match training)
class_names = ['pants', 'shirt', 'shoes']

IMG_SIZE = 224

def predict_image(img_path):
    if not os.path.exists(img_path):
        raise FileNotFoundError("Image not found")

    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]

    return predicted_class


# -------- TEST IMAGE --------
test_image_path =  "data/deepfashion/test/images/pants/img2.jpg"

   # change if needed

result = predict_image(test_image_path)
print("Predicted clothing type:", result)
