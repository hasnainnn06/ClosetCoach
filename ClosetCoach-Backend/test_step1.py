from wardrobe.userWardrobeManager import UserWardrobeManager

uwm = UserWardrobeManager()

print("Images dir:", uwm.images_dir)
print("Wardrobe exists:", uwm.metadata_path.exists())
