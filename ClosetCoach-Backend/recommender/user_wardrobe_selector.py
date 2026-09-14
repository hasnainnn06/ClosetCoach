import random
from wardrobe.userWardrobeManager import UserWardrobeManager


class UserWardrobeSelector:
    """
    Selects outfit items strictly from a user's wardrobe
    using rule-based category filtering.
    """

    def __init__(self, user_id="default_user"):
        self.uwm = UserWardrobeManager(user_id=user_id)
        data = self.uwm.load_wardrobe()
        self.metadata = data["metadata"]

    def select_item(self, category):
        """
        Select a random item from user wardrobe
        matching the required category.
        """
        candidates = [
            item for item, meta in self.metadata.items()
            if meta["category"] == category
        ]

        if not candidates:
            return None

        return random.choice(candidates)

    def generate_outfit(self, required_categories):
        """
        required_categories: list like ['top', 'pants', 'jacket']
        """
        outfit = {}

        for cat in required_categories:
            item = self.select_item(cat)
            if item:
                outfit[cat] = item

        return outfit
