import json
import random

with open("data/polyvore/parsed_outfits.json", "r") as f:
    outfits = json.load(f)

positive_pairs = []
negative_pairs = []

for outfit in outfits:
    items = outfit["items"]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            positive_pairs.append((items[i]["item_id"], items[j]["item_id"], 1))

all_items = [item for outfit in outfits for item in outfit["items"]]

for _ in range(len(positive_pairs)):
    i1, i2 = random.sample(all_items, 2)
    negative_pairs.append((i1["item_id"], i2["item_id"], 0))

pairs = positive_pairs + negative_pairs

with open("data/polyvore/compatibility_pairs.json", "w") as f:
    json.dump(pairs, f)

print("Compatibility pairs generated.")