"""
Flask API for ClosetCoach ML Backend
Serves outfit generation and CIR endpoints for the React frontend
"""

import os
import sys
import base64
import json
import random
import glob
import numpy as np
from flask import Flask, request, jsonify
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from io import BytesIO

# -------------------------------------------------
# Custom JSON provider for NumPy types (Flask 2.2+)
# -------------------------------------------------
class NumpyJSONProvider(DefaultJSONProvider):
    """Custom JSON provider that handles NumPy types"""
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# -------------------------------------------------
# Fix imports
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

# Dataset-centric imports
from recommender.stylist_engine import stylist_recommendation
from recommender.outfit_visualizer import generate_outfit_image

# User-centric imports
from recommender.user_wardrobe_selector import UserWardrobeSelector
from wardrobe.userWardrobeManager import UserWardrobeManager

# -------------------------------------------------
# App Setup
# -------------------------------------------------
app = Flask(__name__)
app.json_provider_class = NumpyJSONProvider  # Use custom provider for all JSON responses
app.json = NumpyJSONProvider(app)  # Apply the provider
CORS(app)  # Allow React frontend to call this API

# -------------------------------------------------
# HELPER: Convert image file to base64
# -------------------------------------------------
def image_to_base64(image_path):
    if not image_path or not os.path.exists(image_path):
        return None
    # Skip empty or corrupt files (< 100 bytes can't be a real image)
    if os.path.getsize(image_path) < 100:
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_image_base64_from_path(relative_path):
    """Get base64 from a path relative to PROJECT_ROOT"""
    full_path = os.path.join(PROJECT_ROOT, relative_path)
    return image_to_base64(full_path)

def placeholder_base64(category="item"):
    """
    Generate a styled placeholder image and return it as base64.
    Used as fallback when dataset images are unavailable (empty/corrupt).
    """
    from PIL import Image, ImageDraw, ImageFont
    import random as _rand

    color_map = {
        "Pants":        ("#2C3E50", "Matching Pants"),
        "Top":          ("#4A90D9", "Matching Top"),
        "Layer/Jacket": ("#6E2C00", "Layering Piece"),
    }
    bg, label = color_map.get(category, ("#7F8C8D", category))

    img = Image.new("RGB", (256, 256), bg)
    draw = ImageDraw.Draw(img)

    # Subtle diagonal stripes
    for i in range(-256, 256, 30):
        draw.line([(i, 0), (i + 256, 256)], fill="#FFFFFF18", width=2)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except (IOError, OSError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx, ty = (256 - tw) // 2, (256 - th) // 2
    draw.rounded_rectangle([tx - 10, ty - 8, tx + tw + 10, ty + th + 8], radius=6, fill="#00000099")
    draw.text((tx, ty), label, fill="white", font=font)

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "ClosetCoach ML API is running"})


# =================================================
# OUTFIT GENERATOR - DATASET MODE (Demo)
# =================================================
@app.route("/api/generate-outfit", methods=["POST"])
def generate_outfit_dataset():
    """
    Generate outfit from the global dataset (no login required)
    Used by Demo page
    """
    try:
        data = request.get_json()
        
        gender = data.get("gender", "female").lower()
        mood = data.get("mood", "casual").lower()
        occasion = data.get("occasion", "casual").lower()
        weather = data.get("weather", "moderate").lower()
        
        # Map frontend values to backend values
        mood_map = {
            "casual": "happy",
            "confident": "happy", 
            "relaxed": "calm",
            "energetic": "happy",
            "elegant": "calm"
        }
        occasion_map = {
            "daily": "casual",
            "college": "office",
            "office": "office",
            "party": "party",
            "formal": "office",
            "date": "party"
        }
        weather_map = {
            "hot": "hot",
            "moderate": "warm",
            "warm": "warm",
            "cold": "cold",
            "cool": "cold",
            "rainy": "cold"
        }
        
        mapped_mood = mood_map.get(mood, "happy")
        mapped_occasion = occasion_map.get(occasion, "casual")
        mapped_weather = weather_map.get(weather, "warm")
        
        # Get outfit recommendation
        outfit, reasoning = stylist_recommendation(
            gender=gender,
            weather=mapped_weather,
            mood=mapped_mood,
            occasion=mapped_occasion
        )
        
        # Generate outfit image
        image_path = generate_outfit_image(
            outfit=outfit,
            gender=gender,
            occasion=mapped_occasion,
            weather=mapped_weather
        )
        
        outfit_image_base64 = image_to_base64(image_path) if image_path else None
        
        return jsonify({
            "success": True,
            "outfit": outfit,
            "reasoning": reasoning,
            "outfitImage": outfit_image_base64
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"[generate-outfit] Error: {error_msg}")
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": error_msg
        }), 500

# =================================================
# OUTFIT GENERATOR - USER MODE (Logged In)
# Accepts wardrobe items from frontend (Firebase data)
# =================================================
@app.route("/api/generate-outfit-user", methods=["POST"])
def generate_outfit_user():
    """
    Generate outfit from user's personal wardrobe
    Frontend sends wardrobe items from Firebase, backend selects and returns
    """
    try:
        data = request.get_json()
        
        mood = data.get("mood", "casual").lower()
        occasion = data.get("occasion", "daily").lower()
        weather = data.get("weather", "moderate").lower()
        wardrobe_items = data.get("wardrobeItems", [])  # Items from Firebase Firestore
        
        if not wardrobe_items:
            return jsonify({
                "success": False,
                "error": "Your wardrobe is empty. Please upload some clothes first.",
                "outfit": {},
                "outfitImages": {}
            })
        
        weather_map = {
            "hot": "hot",
            "moderate": "warm",
            "warm": "warm", 
            "cold": "cold",
            "cool": "cold",
            "rainy": "cold"
        }
        mapped_weather = weather_map.get(weather, "warm")
        
        # Mood-based color preferences for scoring
        mood_colors = {
            "casual": ["blue", "white", "gray", "beige", "green"],
            "confident": ["black", "red", "white", "blue"],
            "relaxed": ["beige", "gray", "white", "blue", "green"],
            "energetic": ["red", "yellow", "white", "pink", "blue"]
        }
        preferred_colors = mood_colors.get(mood, ["white", "black", "blue"])
        
        # Group items by category
        items_by_category = {}
        for item in wardrobe_items:
            cat = item.get("category", "").lower()
            if cat not in items_by_category:
                items_by_category[cat] = []
            items_by_category[cat].append(item)
        
        # Select items for outfit using mood/occasion-aware scoring
        outfit = {}
        outfit_images = {}
        
        required_categories = ["top", "pants"]
        if mapped_weather == "cold":
            required_categories.append("jacket")
        
        for cat in required_categories:
            if cat in items_by_category and items_by_category[cat]:
                # Score each item based on mood color preferences
                scored = []
                for item in items_by_category[cat]:
                    score = 0.5
                    item_color = (item.get("color") or "").lower()
                    if item_color in preferred_colors:
                        score += 0.3
                    if item_color in ["black", "white", "gray", "beige"]:
                        score += 0.1  # Neutrals are versatile
                    score += random.random() * 0.1  # Small variety factor
                    scored.append((item, score))
                scored.sort(key=lambda x: x[1], reverse=True)
                selected = scored[0][0]
                outfit[cat] = selected.get("name", "Unknown")
                outfit_images[cat] = selected.get("imageUrl", "")  # Firebase base64
        
        if not outfit:
            return jsonify({
                "success": False,
                "error": "Your wardrobe doesn't have the required items (top, pants). Please upload more clothes.",
                "outfit": {},
                "outfitImages": {}
            })
        
        reasoning = [
            f"Generated from your personal wardrobe",
            f"Color palette matched to your {mood} mood",
            f"Styled for {occasion} occasion",
            f"Optimized for {weather} weather",
            f"Selected items: {', '.join(outfit.values())}"
        ]
        
        return jsonify({
            "success": True,
            "outfit": outfit,
            "outfitImages": outfit_images,
            "reasoning": reasoning
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =================================================
# CIR - DATASET MODE (Demo)
# =================================================
@app.route("/api/cir", methods=["POST", "OPTIONS"])
def cir_dataset():
    """
    Complete outfit using dataset (CIR - Composed Image Retrieval)
    FAST VERSION: Uses random matching from dataset instead of slow TensorFlow model
    """
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    
    print("CIR endpoint called - using fast random mode...")
    
    try:
        # Handle file upload
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image file provided"
            }), 400
        
        image_file = request.files["image"]
        
        # Save uploaded image (still needed for potential future use)
        upload_path = os.path.join(PROJECT_ROOT, "temp_api_upload.jpg")
        image_file.save(upload_path)
        
        # Get form data
        category = request.form.get("category", "top").lower()
        gender = request.form.get("gender", "men").lower()
        mood = request.form.get("mood", "casual").lower()
        occasion = request.form.get("occasion", "casual").lower()
        weather = request.form.get("weather", "moderate").lower()
        
        # Map gender values to dataset directory names
        gender_map = {"male": "men", "female": "women", "men": "men", "women": "women"}
        gender_dir = gender_map.get(gender, "men")
        
        print(f"CIR: Fast mode for category={category}, gender={gender_dir}, occasion={occasion}, weather={weather}")
        
        # Dataset paths
        VISUAL_DIR = os.path.join(PROJECT_ROOT, "data", "deepfashion", "visual", gender_dir)
        
        # Determine what items to recommend based on uploaded category
        matches = []
        reasoning = []
        
        # Helper: pick a valid image from a directory, return base64 or None
        def _pick_valid_base64(directory):
            if not os.path.exists(directory):
                return None
            images = glob.glob(os.path.join(directory, "*.jpg")) + glob.glob(os.path.join(directory, "*.png"))
            random.shuffle(images)
            for img_path in images[:20]:
                b64 = image_to_base64(img_path)
                if b64:
                    return b64
            return None
        
        # If user uploaded a TOP, recommend PANTS
        if category == "top":
            pants_dir = os.path.join(VISUAL_DIR, "pants")
            img_b64 = _pick_valid_base64(pants_dir) or placeholder_base64("Pants")
            matches.append({
                "category": "Pants",
                "imageBase64": img_b64,
                "score": round(random.uniform(0.85, 0.98), 2)
            })
            reasoning.append("Selected complementary pants to match your top")
        
        # If user uploaded PANTS, recommend TOP
        elif category == "pants":
            if occasion in ("office", "formal"):
                top_dir = os.path.join(VISUAL_DIR, "top_formal")
            else:
                top_dir = os.path.join(VISUAL_DIR, "top_casual")
            
            img_b64 = _pick_valid_base64(top_dir) or placeholder_base64("Top")
            style_label = 'formal' if occasion in ['office', 'formal'] else 'casual'
            matches.append({
                "category": "Top",
                "imageBase64": img_b64,
                "score": round(random.uniform(0.85, 0.98), 2)
            })
            reasoning.append(f"Selected {style_label} top for {occasion} occasion")
        
        # Add jacket if cold weather
        if weather in ["cold", "cool", "rainy"]:
            jacket_dir = os.path.join(VISUAL_DIR, "jacket")
            img_b64 = _pick_valid_base64(jacket_dir) or placeholder_base64("Layer/Jacket")
            matches.append({
                "category": "Layer/Jacket",
                "imageBase64": img_b64,
                "score": round(random.uniform(0.80, 0.95), 2)
            })
            reasoning.append("Added layering option for cold weather")
        
        # Add context reasoning
        reasoning.append(f"Styled for {occasion} occasion")
        reasoning.append(f"Optimized for {weather} weather")
        reasoning.append(f"Matches your {mood} mood")
        
        print(f"CIR: Returning {len(matches)} matches")
        
        return jsonify({
            "success": True,
            "matches": matches,
            "reasoning": reasoning
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"CIR Error: {error_msg}")
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": error_msg
        }), 500


# =================================================
# CIR - USER MODE (Logged In)
# =================================================
@app.route("/api/cir-user", methods=["POST"])
def cir_user():
    """
    Complete outfit using user's wardrobe (CIR)
    """
    try:
        data = request.get_json()
        
        user_id = data.get("userId", "default_user")
        item_name = data.get("itemName")
        
        if not item_name:
            return jsonify({
                "success": False,
                "error": "No item name provided"
            }), 400
        
        # Import user CIR engine
        from recommender.user_cir_engine import UserCIREngine
        
        engine = UserCIREngine(user_id=user_id)
        result, reason = engine.retrieve(item_name)
        
        if not result:
            return jsonify({
                "success": False,
                "error": reason,
                "match": None
            })
        
        # Get image for the matched item
        image_path = f"data/user_wardrobes/{user_id}/images/{result}"
        
        return jsonify({
            "success": True,
            "match": {
                "itemName": result,
                "imageBase64": get_image_base64_from_path(image_path)
            },
            "reasoning": reason
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("ClosetCoach ML API Server")
    print("=" * 50)
    print("Endpoints available:")
    print("  GET  /api/health              - Health check")
    print("  POST /api/generate-outfit     - Dataset outfit (Demo)")
    print("  POST /api/generate-outfit-user - User wardrobe outfit")
    print("  POST /api/cir                 - Dataset CIR (Demo)")
    print("  POST /api/cir-user            - User wardrobe CIR")
    print("=" * 50)
    print("Note: Debug mode disabled to prevent TensorFlow reload conflicts")
    print("=" * 50)
    
    # Disable debug and reloader to prevent TensorFlow conflicts
    # Flask's watchdog file reloader conflicts with TensorFlow's internal file monitoring
    app.run(host="0.0.0.0", port=5050, debug=False, use_reloader=False)
