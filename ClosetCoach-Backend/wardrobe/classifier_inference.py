import tensorflow as tf
import numpy as np

CLASSIFIER_MODEL_PATH = "models/closetcoach_cnn.h5"

_classifier = None
_class_names = ['dress', 'jacket', 'pants', 'shorts', 'skirt', 'top']

def load_classifier():
    global _classifier
    if _classifier is None:
        _classifier = tf.keras.models.load_model(CLASSIFIER_MODEL_PATH)
    return _classifier


def predict_category(image_tensor):
    model = load_classifier()
    preds = model.predict(image_tensor, verbose=0)
    class_idx = np.argmax(preds)
    return _class_names[class_idx]
