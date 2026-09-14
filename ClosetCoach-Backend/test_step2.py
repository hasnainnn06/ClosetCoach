from wardrobe.wardrobe_inference import WardrobeInference

wi = WardrobeInference()

result = wi.analyze_image("temp_upload.jpg")

print("Category:", result["category"])
print("Colors:", result["colors"])
print("Embedding shape:", result["embedding"].shape)
