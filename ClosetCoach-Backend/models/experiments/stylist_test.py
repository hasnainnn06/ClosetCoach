import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from recommender.stylist_engine import stylist_recommendation


test_cases = [
    {
        "gender": "male",
        "weather": "hot",
        "mood": "calm",
        "occasion": "casual"
    },
    {
        "gender": "female",
        "weather": "cold",
        "mood": "sad",
        "occasion": "office"
    },
    {
        "gender": "female",
        "weather": "warm",
        "mood": "happy",
        "occasion": "party"
    }
]

for i, case in enumerate(test_cases, 1):
    print(f"\n=== TEST CASE {i} ===")
    outfit, reason = stylist_recommendation(**case)

    print("Input:", case)
    print("\nRecommended Outfit:")
    for k, v in outfit.items():
        print(f"- {k}: {v}")

    print("\nReasoning:")
    for r in reason:
        print("-", r)
