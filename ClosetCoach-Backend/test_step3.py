from wardrobe.wardrobe_inference import WardrobeInference
from wardrobe.userWardrobeManager import UserWardrobeManager

wi = WardrobeInference()
uwm = UserWardrobeManager()

result = wi.analyze_image("temp_upload.jpg")

uwm.add_item(
    source_image_path="temp_upload.jpg",
    item_name="item_001.jpg",
    category=result["category"],
    colors=result["colors"],
    embedding=result["embedding"]
)

wardrobe = uwm.load_wardrobe()

print("Stored items:", wardrobe["metadata"].keys())
print("Embedding count:", len(wardrobe["embeddings"]))
