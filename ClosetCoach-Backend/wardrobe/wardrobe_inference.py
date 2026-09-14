from wardrobe.image_inference_preprocess import preprocess_for_inference
from preprocessing.color_extraction import extract_colors
from wardrobe.embedding_inference import get_embedding
from wardrobe.classifier_inference import predict_category


class WardrobeInference:
    """
    Runs inference on a single clothing image uploaded by user.
    """

    def analyze_image(self, image_path):
        image_tensor = preprocess_for_inference(image_path)

        category = predict_category(image_tensor)
        colors = extract_colors(image_path)
        embedding = get_embedding(image_tensor)

        return {
            "category": category,
            "colors": colors,
            "embedding": embedding
        }
