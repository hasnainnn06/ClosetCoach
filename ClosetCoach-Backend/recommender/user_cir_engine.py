import numpy as np
from wardrobe.userWardrobeManager import UserWardrobeManager


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class UserCIREngine:
    """
    Complementary Item Retrieval using ONLY user's wardrobe.
    """

    def __init__(self, user_id="default_user"):
        self.uwm = UserWardrobeManager(user_id=user_id)
        data = self.uwm.load_wardrobe()
        self.metadata = data["metadata"]
        self.embeddings = data["embeddings"]

    def _get_missing_category(self, given_category):
        """
        Rule-based category completion.
        """
        rules = {
            "top": "pants",
            "pants": "top",
            "jacket": "top",
            "dress": "jacket"
        }
        return rules.get(given_category)

    def retrieve(self, given_item_name):
        """
        Returns the most compatible complementary item.
        """
        if given_item_name not in self.metadata:
            return None, "Item not found in user wardrobe"

        given_category = self.metadata[given_item_name]["category"]
        missing_category = self._get_missing_category(given_category)

        if not missing_category:
            return None, "No completion rule for this category"

        given_embedding = self.embeddings[given_item_name]

        candidates = {
            item: emb
            for item, emb in self.embeddings.items()
            if self.metadata[item]["category"] == missing_category
        }

        if not candidates:
            return None, "No suitable item in wardrobe"

        best_item = None
        best_score = -1

        for item, emb in candidates.items():
            score = cosine_similarity(given_embedding, emb)
            if score > best_score:
                best_score = score
                best_item = item

        return best_item, f"Matched based on visual compatibility (cosine similarity = {best_score:.2f})"
