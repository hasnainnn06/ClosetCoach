import os
import random
from PIL import Image, ImageDraw, ImageFont

# Compute absolute base path relative to THIS file's location
# This ensures paths resolve correctly regardless of where Flask is launched from
_THIS_DIR = os.path.abspath(os.path.dirname(__file__))
_BACKEND_ROOT = os.path.abspath(os.path.join(_THIS_DIR, os.pardir))


def normalize_gender(gender):
    gender = gender.lower()
    if gender in ["female", "women", "woman"]:
        return "women"
    if gender in ["male", "men", "man"]:
        return "men"
    raise ValueError(f"Invalid gender: '{gender}'. Expected male/female/men/women.")


def pick_image(folder, max_retries=20):
    """
    Pick a random valid image from the given folder.
    Validates the image is openable by PIL to handle corrupt/empty files.
    Returns absolute path or None.
    """
    if not os.path.exists(folder):
        return None

    imgs = [
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    if not imgs:
        return None

    # Shuffle and try images until we find a valid one
    random.shuffle(imgs)
    for img_name in imgs[:max_retries]:
        img_path = os.path.join(folder, img_name)
        try:
            # Reject empty files quickly
            if os.path.getsize(img_path) < 100:
                continue
            # Validate the image is readable
            with Image.open(img_path) as test_img:
                test_img.verify()
            return img_path
        except Exception:
            continue

    return None


# ---------------------------------------------------------------
# Fallback: Generate styled placeholder images when dataset images
# are unavailable (e.g., not downloaded, corrupt, or empty).
# ---------------------------------------------------------------

# Color schemes per category for visually appealing placeholders
_PLACEHOLDER_COLORS = {
    "top": {
        "casual": [
            {"bg": "#4A90D9", "accent": "#6CB4EE", "label": "Casual Top"},
            {"bg": "#E8A87C", "accent": "#F4C7AB", "label": "Cotton Tee"},
            {"bg": "#85C88A", "accent": "#A8D8A8", "label": "Relaxed Fit"},
        ],
        "office": [
            {"bg": "#2C3E50", "accent": "#34495E", "label": "Formal Shirt"},
            {"bg": "#ECF0F1", "accent": "#BDC3C7", "label": "Oxford Shirt"},
            {"bg": "#7F8C8D", "accent": "#95A5A6", "label": "Button-Down"},
        ],
        "party": [
            {"bg": "#8E44AD", "accent": "#9B59B6", "label": "Statement Top"},
            {"bg": "#C0392B", "accent": "#E74C3C", "label": "Bold Top"},
        ],
    },
    "pants": {
        "default": [
            {"bg": "#2C3E50", "accent": "#34495E", "label": "Dark Jeans"},
            {"bg": "#D4A574", "accent": "#C4956A", "label": "Chinos"},
            {"bg": "#5D6D7E", "accent": "#6C7A89", "label": "Tailored Pants"},
            {"bg": "#1A5276", "accent": "#2471A3", "label": "Slim Fit"},
        ],
    },
    "jacket": {
        "default": [
            {"bg": "#1C2833", "accent": "#2C3E50", "label": "Classic Jacket"},
            {"bg": "#6E2C00", "accent": "#873600", "label": "Leather Jacket"},
            {"bg": "#566573", "accent": "#707B7C", "label": "Bomber Jacket"},
        ],
    },
}


def _generate_placeholder(category, occasion="casual", size=(256, 256)):
    """
    Generate a stylish placeholder image for a clothing category.
    Returns a PIL Image object.
    """
    pool = _PLACEHOLDER_COLORS.get(category, {})
    options = pool.get(occasion, pool.get("default", [{"bg": "#AAB7B8", "accent": "#D5DBDB", "label": category.title()}]))
    style = random.choice(options)

    bg_color = style["bg"]
    accent_color = style["accent"]
    label = style["label"]

    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    # Draw a subtle pattern (diagonal stripes for visual interest)
    w, h = size
    for i in range(-h, w, 30):
        draw.line([(i, 0), (i + h, h)], fill=accent_color, width=2)

    # Draw a centered label with background
    text = label
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except (IOError, OSError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (w - text_w) // 2
    text_y = (h - text_h) // 2

    # Text background pill
    padding = 12
    draw.rounded_rectangle(
        [text_x - padding, text_y - padding, text_x + text_w + padding, text_y + text_h + padding],
        radius=8,
        fill=(0, 0, 0, 180) if hasattr(draw, 'rounded_rectangle') else "#000000"
    )
    draw.text((text_x, text_y), text, fill="white", font=font)

    # Small "AI Generated" watermark at the bottom
    try:
        small_font = ImageFont.truetype("arial.ttf", 10)
    except (IOError, OSError):
        small_font = ImageFont.load_default()
    draw.text((8, h - 18), "AI Placeholder", fill="#FFFFFF80", font=small_font)

    return img


def labeled_block(image, label, size=(256, 256)):
    """Create a labeled image block with a header bar."""
    image = image.resize(size)
    canvas = Image.new("RGB", (size[0], size[1] + 40), "white")
    canvas.paste(image, (0, 40))

    draw = ImageDraw.Draw(canvas)
    draw.rectangle([(0, 0), (size[0], 40)], fill=(240, 240, 240))
    draw.text((10, 10), label, fill="black")

    return canvas


def generate_outfit_image(outfit, gender, occasion, weather):
    """
    Generate a composite outfit image by picking random items from the dataset.
    Falls back to styled placeholder images when dataset images are unavailable.

    Args:
        outfit: Dict with outfit components (from stylist_engine)
        gender: 'male'/'female'/'men'/'women'
        occasion: 'casual'/'office'/'party'
        weather: 'hot'/'warm'/'cold'

    Returns:
        Absolute path to the generated outfit image, or None on total failure.
    """
    gender = normalize_gender(gender)
    base = os.path.join(_BACKEND_ROOT, "data", "deepfashion", "visual", gender)

    blocks = []

    # --- TOP ---
    # Use occasion-aware top selection for better recommendations
    if occasion in ("office", "formal"):
        top_folder = os.path.join(base, "top_formal")
        if not os.path.exists(top_folder) or not os.listdir(top_folder):
            top_folder = os.path.join(base, "top")
    else:
        top_folder = os.path.join(base, "top")

    top_img = pick_image(top_folder)
    if top_img:
        try:
            blocks.append(labeled_block(Image.open(top_img), "TOP"))
        except Exception:
            top_img = None

    # Fallback to placeholder if no valid dataset image
    if not top_img:
        placeholder = _generate_placeholder("top", occasion)
        blocks.append(labeled_block(placeholder, "TOP"))

    # --- BOTTOM ---
    bottom_img = pick_image(os.path.join(base, "pants"))
    if bottom_img:
        try:
            blocks.append(labeled_block(Image.open(bottom_img), "BOTTOM"))
        except Exception:
            bottom_img = None

    if not bottom_img:
        placeholder = _generate_placeholder("pants", occasion)
        blocks.append(labeled_block(placeholder, "BOTTOM"))

    # --- LAYER (cold weather only) ---
    if weather == "cold":
        layer_img = pick_image(os.path.join(base, "jacket"))
        if layer_img:
            try:
                blocks.append(labeled_block(Image.open(layer_img), "LAYER"))
            except Exception:
                layer_img = None

        if not layer_img:
            placeholder = _generate_placeholder("jacket")
            blocks.append(labeled_block(placeholder, "LAYER"))

    if not blocks:
        return None

    # --- COMPOSE FINAL IMAGE ---
    width = blocks[0].width
    height = sum(b.height for b in blocks)

    final_img = Image.new("RGB", (width, height), "white")

    y = 0
    for b in blocks:
        final_img.paste(b, (0, y))
        y += b.height

    # Save to an absolute path inside the backend directory
    output = os.path.join(_BACKEND_ROOT, "final_outfit.png")
    final_img.save(output)
    return output
