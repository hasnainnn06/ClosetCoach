import json

labels = [
    "tshirt",
    "shirt",
    "jacket",
    "pants",
    "dress",
    "shoes",
    "bag"
]

label_map = {label: idx for idx, label in enumerate(labels)}

with open("data/deepfashion/label_map.json", "w") as f:
    json.dump(label_map, f, indent=4)

print("Label encoding saved!")
