import json

INPUT_FILE = "data/polyvore/outfits.json"
OUTPUT_FILE = "data/polyvore/parsed_outfits.json"

with open(INPUT_FILE, "r") as f:
    outfits = json.load(f)

parsed_outfits = []

for outfit in outfits:
    items = []
    for item in outfit["items"]:
        items.append({
            "item_id": item["item_id"],
            "category": item["category"],
            "image": item["image"]
        })
    parsed_outfits.append({
        "outfit_id": outfit["outfit_id"],
        "items": items
    })

with open(OUTPUT_FILE, "w") as f:
    json.dump(parsed_outfits, f, indent=2)

print("Polyvore outfits parsed successfully.")
