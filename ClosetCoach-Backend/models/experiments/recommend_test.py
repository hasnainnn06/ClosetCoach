import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from recommender.rule_engine import recommend_outfit


# -------- TEST INPUTS --------
detected_item = "shoes"
dominant_colors = ["white", "brown"]

weather = "hot"
mood = "positive"
occasion = "casual"

outfit, reasons = recommend_outfit(
    detected_item,
    dominant_colors,
    weather,
    mood,
    occasion
)

print("Detected item:", detected_item)
print("Dominant colors:", dominant_colors)

print("\nRecommended outfit:")
for o in outfit:
    print("-", o)

print("\nReasoning:")
for r in reasons:
    print("-", r)
