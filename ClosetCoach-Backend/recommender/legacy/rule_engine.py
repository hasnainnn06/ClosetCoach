def recommend_outfit(item, colors, weather, mood, occasion):
    outfit = []
    reason = []

    # ---- Weather rules ----
    if weather == "hot":
        outfit.append("light cotton top")
        reason.append("hot weather requires breathable fabrics")
    elif weather == "cold":
        outfit.append("jacket or sweater")
        reason.append("cold weather requires warm clothing")

    # ---- Mood rules ----
    if mood == "positive":
        reason.append("bright colors match positive mood")
    elif mood == "calm":
        reason.append("soft colors suit calm mood")

    # ---- Occasion rules ----
    if occasion == "casual":
        outfit.append("jeans or chinos")
        reason.append("casual occasion prefers comfort")
    elif occasion == "office":
        outfit.append("formal shirt and trousers")
        reason.append("office wear requires formality")
    elif occasion == "party":
        outfit.append("stylish outfit")
        reason.append("party wear should be trendy")

    # ---- Item-based logic ----
    if item == "shoes":
        outfit.insert(0, "matching top and bottom")
        reason.append("shoes should complement the outfit")
    elif item == "shirt":
        outfit.append("matching pants and shoes")
    elif item == "pants":
        outfit.append("matching shirt and shoes")

    return outfit, reason
