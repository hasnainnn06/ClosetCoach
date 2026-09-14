import tensorflow as tf
import numpy as np

EMBEDDING_MODEL_PATH = "models/embedding_model.h5"

_embedding_model = None

def load_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = tf.keras.models.load_model(EMBEDDING_MODEL_PATH)
    return _embedding_model


def get_embedding(image_tensor):
    """
    image_tensor: shape (1, 224, 224, 3)
    returns: 1D numpy embedding vector
    """
    model = load_embedding_model()
    embedding = model.predict(image_tensor, verbose=0)
    return embedding.flatten()
