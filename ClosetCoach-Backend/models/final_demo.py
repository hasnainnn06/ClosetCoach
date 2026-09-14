import sys
import os

# -------------------------------------------------
# Fix Python path (so recommender module is found)
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from recommender.stylist_engine import stylist_recommendation
from recommender.outfit_visualizer import generate_outfit_image

# -------------------------------------------------
# USER INPUT (can later be replaced by UI)
# -------------------------------------------------
gender = "female"   # user input

# Map user gender to dataset folder
gender_map = {
    "male": "men",
    "female": "women"
}

dataset_gender = gender_map.get(gender.lower())
    # male / female
weather = "cold"       # hot / warm / cold
mood = "sad"           # happy / calm / sad / angry / neutral
occasion = "office"    # casual / office / party

# -------------------------------------------------
# STEP 1: HUMAN STYLIST LOGIC
# -------------------------------------------------
outfit, reasoning = stylist_recommendation(
    gender=gender,
    weather=weather,
    mood=mood,
    occasion=occasion
)

print("\n=== CLOSETCOACH STYLIST OUTPUT ===")
for k, v in outfit.items():
    print(f"{k}: {v}")

print("\nReasoning:")
for r in reasoning:
    print("-", r)

# -------------------------------------------------
# STEP 2: VISUAL OUTFIT GENERATION (GENDER + OCCASION SAFE)
# -------------------------------------------------
final_image_path = generate_outfit_image(
    outfit=outfit,
    gender=gender,
    occasion=occasion,
    weather=weather
)

if final_image_path:
    print(f"\n🖼 Final outfit image generated: {final_image_path}")

    # Auto-open image on Windows (optional but useful)
    try:
        os.startfile(final_image_path)
    except:
        pass
else:
    print("\n❌ Failed to generate outfit image")
