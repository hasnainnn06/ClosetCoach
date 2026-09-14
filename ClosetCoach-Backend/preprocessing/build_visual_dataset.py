import os
import shutil

SOURCE = "data/deepfashion/img_highres"
TARGET = "data/deepfashion/visual"

FORMAL_TOP_KEYWORDS = ["Shirts", "Polos", "Blouses"]
CASUAL_TOP_KEYWORDS = ["Tees", "Tanks", "Graphic"]

def is_front(img):
    return "front" in img.lower()

for gender in ["MEN", "WOMEN"]:
    for style in ["top_formal", "top_casual", "pants", "jacket"]:
        os.makedirs(os.path.join(TARGET, gender.lower(), style), exist_ok=True)

    base = os.path.join(SOURCE, gender)

    for root, _, files in os.walk(base):
        for f in files:
            if not f.lower().endswith((".jpg", ".jpeg")):
                continue
            if not is_front(f):
                continue

            src = os.path.join(root, f)
            root_lower = root.lower()

            if any(k.lower() in root_lower for k in FORMAL_TOP_KEYWORDS):
                shutil.copy(src, os.path.join(TARGET, gender.lower(), "top_formal"))
            elif any(k.lower() in root_lower for k in CASUAL_TOP_KEYWORDS):
                shutil.copy(src, os.path.join(TARGET, gender.lower(), "top_casual"))
            elif "pants" in root_lower or "denim" in root_lower:
                shutil.copy(src, os.path.join(TARGET, gender.lower(), "pants"))
            elif "jacket" in root_lower or "coat" in root_lower:
                shutil.copy(src, os.path.join(TARGET, gender.lower(), "jacket"))

print("✅ Visual dataset rebuilt with FORMAL / CASUAL separation")
