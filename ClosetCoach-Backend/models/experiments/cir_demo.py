import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from recommender.cir_engine import recommend_complementary
from recommender.outfit_visualizer import labeled_block
from PIL import Image

# ---------------- USER INPUT ----------------
uploaded_image = "sample_upload.jpg"  # replace with real image
gender = "women"
uploaded_category = "top"  # top / pants / jacket

# ---------------- CATEGORY LOGIC ----------------
if uploaded_category == "top":
    target = "pants"
elif uploaded_category == "pants":
    target = "top"
else:
    target = "top"

# ---------------- CIR ----------------
results = recommend_complementary(
    uploaded_image,
    gender=gender,
    target_category=target
)

blocks = []
blocks.append(
    labeled_block(Image.open(uploaded_image), "UPLOADED ITEM")
)

for path, score in results:
    blocks.append(
        labeled_block(Image.open(path), f"RECOMMENDED ({score:.2f})")
    )

# ---------------- COMPOSE ----------------
width = blocks[0].width
height = sum(b.height for b in blocks)

final = Image.new("RGB", (width, height), "white")
y = 0
for b in blocks:
    final.paste(b, (0, y))
    y += b.height

final.save("cir_output.png")
print("🧩 CIR outfit generated: cir_output.png")
