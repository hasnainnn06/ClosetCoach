import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from recommender.cir_engine import recommend_complementary

input_image = "data/deepfashion/test/images/img4.jpeg"
dataset_folder = "data/deepfashion/train/images"

results = recommend_complementary(input_image, dataset_folder)

print("Input item:", input_image)
print("\nRecommended complementary items:")

for item, score in results:
    print(f"- {item} (similarity: {score:.2f})")
