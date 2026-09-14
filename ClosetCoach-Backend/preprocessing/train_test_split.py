import os
import random
import shutil

SOURCE_DIR = "data/deepfashion/processed_images"
TRAIN_DIR = "data/deepfashion/train/images"
TEST_DIR = "data/deepfashion/test/images"

os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)

images = os.listdir(SOURCE_DIR)

# safety check
if len(images) == 0:
    raise ValueError("No images found to split")

random.shuffle(images)

split_index = int(0.8 * len(images))

train_images = images[:split_index]
test_images = images[split_index:]

for img in train_images:
    shutil.copy(
        os.path.join(SOURCE_DIR, img),
        os.path.join(TRAIN_DIR, img)
    )

for img in test_images:
    shutil.copy(
        os.path.join(SOURCE_DIR, img),
        os.path.join(TEST_DIR, img)
    )

print("Train images:", len(train_images))
print("Test images:", len(test_images))
