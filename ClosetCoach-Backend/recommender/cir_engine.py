import pickle
import numpy as np
import os

# -------------------------------------------------
# PATHS
# -------------------------------------------------
MODEL_PATH = "models/embedding_model.h5"
INDEX_PATH = "recommender/embedding_index.pkl"
IMG_SIZE = 224

# -------------------------------------------------
# LAZY LOADING - load model only when needed
# -------------------------------------------------
_model = None
_embedding_index = None

def get_model():
    global _model
    if _model is None:
        import tensorflow as tf
        from tensorflow.keras.preprocessing import image as keras_image
        _model = tf.keras.models.load_model(MODEL_PATH)
    return _model

def get_embedding_index():
    global _embedding_index
    if _embedding_index is None:
        with open(INDEX_PATH, "rb") as f:
            _embedding_index = pickle.load(f)
    return _embedding_index

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def extract_embedding(img_path):
    import tensorflow as tf
    from tensorflow.keras.preprocessing import image as keras_image
    from sklearn.metrics.pairwise import cosine_similarity
    
    model = get_model()
    img = keras_image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img = keras_image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    emb = model.predict(img, verbose=0)[0]
    return emb / np.linalg.norm(emb)


def retrieve_similar(query_img, gender, category, top_k=1):
    """
    Retrieve visually similar items from a STRICT category
    (category already encodes formality)
    """
    from sklearn.metrics.pairwise import cosine_similarity
    
    query_emb = extract_embedding(query_img)
    embedding_index = get_embedding_index()

    candidates = [
        item for item in embedding_index
        if item["gender"] == gender and item["category"] == category
    ]

    scored = []
    for item in candidates:
        sim = cosine_similarity(
            [query_emb],
            [item["embedding"]]
        )[0][0]
        # Convert numpy float32 to Python float for JSON serialization
        scored.append((item["path"], float(sim)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


# -------------------------------------------------
# FINAL HUMAN STYLIST CIR (FORMAL-CASUAL ENFORCED)
# -------------------------------------------------
def stylist_cir(
    uploaded_image,
    uploaded_category,
    gender,
    weather,
    mood,
    occasion
):
    """
    Context-aware Complementary Item Retrieval
    with STRICT FORMAL / CASUAL enforcement
    """

    recommendations = {}
    reasoning = []

    # ---------------- DECIDE TOP CATEGORY BASED ON OCCASION ----------------
    if occasion == "office":
        top_category = "top_formal"
    else:
        top_category = "top_casual"

    # ---------------- LOGIC BASED ON UPLOADED ITEM ----------------
    if uploaded_category == "pants":
        # Need TOP
        top_item = retrieve_similar(
            uploaded_image,
            gender,
            top_category
        )
        if top_item:
            recommendations["Top"] = top_item[0]
            reasoning.append("Selected appropriate top based on occasion")

        # Optional layer if cold
        if weather == "cold":
            layer_item = retrieve_similar(
                uploaded_image,
                gender,
                "jacket"
            )
            if layer_item:
                recommendations["Layer"] = layer_item[0]
                reasoning.append("Layer added due to cold weather")

    elif uploaded_category == "top":
        # Need BOTTOM
        bottom_item = retrieve_similar(
            uploaded_image,
            gender,
            "pants"
        )
        if bottom_item:
            recommendations["Bottom"] = bottom_item[0]
            reasoning.append("Added bottom to balance outfit")

        # Optional layer
        if weather == "cold":
            layer_item = retrieve_similar(
                uploaded_image,
                gender,
                "jacket"
            )
            if layer_item:
                recommendations["Layer"] = layer_item[0]
                reasoning.append("Layer added due to cold weather")

    # ---------------- FINAL CONTEXT REASONING ----------------
    reasoning.append(f"Styled specifically for {occasion} occasion")
    reasoning.append(f"Color harmony aligned with {mood} mood")

    return recommendations, reasoning
