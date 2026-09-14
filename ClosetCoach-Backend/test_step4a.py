from recommender.user_wardrobe_selector import UserWardrobeSelector

selector = UserWardrobeSelector()

# Simulate Task-1 decision
required_categories = ["top", "pants"]

outfit = selector.generate_outfit(required_categories)

print("Generated outfit from user wardrobe:")
print(outfit)
