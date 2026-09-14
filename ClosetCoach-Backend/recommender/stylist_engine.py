import random


def stylist_recommendation(gender, weather, mood, occasion):
    """
    AI Stylist Rule Engine — generates outfit recommendations using
    color psychology, weather-appropriateness, and occasion-based styling.

    Args:
        gender:   'male' or 'female'
        weather:  'hot', 'warm', or 'cold'
        mood:     'happy', 'positive', 'calm', 'sad', 'angry', 'neutral'
        occasion: 'casual', 'office', 'party'

    Returns:
        (outfit: dict, reasoning: list[str])
    """

    outfit = {}
    reasoning = []

    # ---------------- NORMALIZE INPUTS ----------------
    gender = gender.lower()
    weather = weather.lower()
    mood = mood.lower()
    occasion = occasion.lower()

    # ---------------- MOOD → COLOR THEORY ----------------
    mood_palette = {
        "happy":    ["white", "yellow", "sky blue", "coral"],
        "positive": ["white", "pastel blue", "light pink"],
        "calm":     ["beige", "grey", "pastel", "sage green"],
        "sad":      ["soft blue", "muted grey", "lavender"],
        "angry":    ["muted tones", "soft neutrals", "olive"],
        "neutral":  ["earth tones", "khaki", "tan"]
    }

    colors = mood_palette.get(mood, ["neutral"])
    reasoning.append(
        f"Color palette ({', '.join(colors)}) selected based on "
        f"'{mood}' mood using color psychology"
    )

    # ---------------- WEATHER RULES ----------------
    if weather == "hot":
        fabric = "cotton / linen"
        layer_allowed = False
        reasoning.append("Hot weather -> breathable fabrics, no heavy layers")

    elif weather == "cold":
        fabric = "wool / fleece"
        layer_allowed = True
        reasoning.append("Cold weather -> warm layers required")

    else:  # warm / moderate
        fabric = "cotton blend"
        layer_allowed = True
        reasoning.append("Moderate weather -> versatile fabric, optional layering")

    # ---------------- OCCASION RULES ----------------
    if occasion == "office":
        base_style = "structured"
        reasoning.append("Office occasion -> clean and formal styling")
    elif occasion == "party":
        base_style = "trendy"
        reasoning.append("Party occasion -> statement and contrast styling")
    else:
        base_style = "casual"
        reasoning.append("Casual occasion -> comfort-first styling")

    # ---------------- GENDER + OCCASION-AWARE SELECTION ----------------
    if gender == "male":
        top_pool = {
            "office":  ["formal shirt", "button-down shirt", "oxford shirt"],
            "party":   ["graphic tee", "polo shirt", "fitted henley"],
            "casual":  ["solid t-shirt", "crew-neck tee", "polo shirt"]
        }
        bottom_pool = {
            "office":  ["chinos", "tailored trousers", "dress pants"],
            "party":   ["slim jeans", "dark wash denim", "chinos"],
            "casual":  ["jeans", "joggers", "chinos"]
        }
        layer_pool = ["bomber jacket", "overshirt", "denim jacket", "blazer"]
    elif gender == "female":
        top_pool = {
            "office":  ["blouse", "fitted top", "structured blazer top"],
            "party":   ["crop top", "off-shoulder top", "satin camisole"],
            "casual":  ["relaxed tee", "fitted top", "knit top"]
        }
        bottom_pool = {
            "office":  ["tailored pants", "pencil skirt", "wide-leg trousers"],
            "party":   ["mini skirt", "leather pants", "flowy skirt"],
            "casual":  ["jeans", "leggings", "cotton pants"]
        }
        layer_pool = ["cardigan", "jacket", "trench coat", "denim jacket"]
    else:
        top_pool = {"casual": ["relaxed top"]}
        bottom_pool = {"casual": ["comfortable bottom"]}
        layer_pool = ["light layer"]

    # Pick from the occasion-specific pool (fallback to casual)
    tops = top_pool.get(occasion, top_pool.get("casual", ["top"]))
    bottoms = bottom_pool.get(occasion, bottom_pool.get("casual", ["bottom"]))

    # Use random.choice for variety across repeated queries
    outfit["Top"] = random.choice(tops)
    outfit["Bottom"] = random.choice(bottoms)

    if layer_allowed:
        outfit["Layer"] = random.choice(layer_pool)

    outfit["Fabric"] = fabric
    outfit["Color Palette"] = colors

    # ---------------- TREND INJECTION ----------------
    trend_options = [
        "minimalist, relaxed fit, earth-tone inspired",
        "athleisure-meets-street, oversized silhouettes",
        "quiet luxury, muted tones, clean lines",
        "classic layering, neutral palette",
        "modern workwear, functional aesthetics"
    ]
    outfit["Trend"] = random.choice(trend_options)
    reasoning.append(f"Incorporated current fashion trend: {outfit['Trend']}")

    return outfit, reasoning