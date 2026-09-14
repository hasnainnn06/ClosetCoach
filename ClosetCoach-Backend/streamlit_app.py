import streamlit as st
import os
import sys
import json

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
from wardrobe.wardrobe_inference import WardrobeInference
from wardrobe.userWardrobeManager import UserWardrobeManager

# -------------------------------------------------
# PAGE CONFIG — DESKTOP FIRST
# -------------------------------------------------
st.set_page_config(
    page_title="ClosetCoach",
    page_icon="👗",
    layout="wide"
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("👗 ClosetCoach")
st.subheader("AI-Powered Smart Wardrobe & Outfit Recommendation System")

st.markdown(
    """
    - 🧥 Generate **complete outfits**
    - 🧩 Complete your outfit intelligently (CIR)
    - 👕 Manage your **personal digital wardrobe**
    """
)

st.divider()

# =================================================
# RECOMMENDATION MODE SELECTOR
# =================================================
st.markdown("## 🎯 Recommendation Mode")

mode = st.radio(
    "",
    ["My Wardrobe (Personalized)", "Global Dataset (Demo Mode)"],
    horizontal=True
)

if mode == "My Wardrobe (Personalized)":
    st.success("Personalized recommendations using **your own wardrobe**.")
else:
    st.info("Demo mode using the trained **global DeepFashion dataset**.")

st.divider()

# -------------------------------------------------
# TABS
# -------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🧥 Outfit Generator",
    "🧩 Complete My Outfit (CIR)",
    "👕 My Wardrobe"
])

# =================================================
# TAB 1 — TASK-1 OUTFIT GENERATOR
# =================================================
with tab1:
    st.header("🧥 Generate My Outfit")

    col1, col2, col3, col4 = st.columns(4)
    gender = col1.selectbox("Gender", ["Female", "Male"])
    weather = col2.selectbox("Weather", ["Hot", "Warm", "Cold"])
    mood = col3.selectbox("Mood", ["Happy", "Calm", "Sad", "Angry", "Neutral"])
    occasion = col4.selectbox("Occasion", ["Casual", "Office", "Party"])

    if st.button("✨ Get My Outfit", use_container_width=True):
        weather_l = weather.lower()
        occasion_l = occasion.lower()

        # -----------------------------
        # USER-CENTRIC MODE
        # -----------------------------
        if mode == "My Wardrobe (Personalized)":
            selector = UserWardrobeSelector()

            required_categories = ["top", "pants"]
            if weather == "Cold":
                required_categories.append("jacket")

            outfit = selector.generate_outfit(required_categories)

            st.subheader("👕 Your Personalized Outfit")

            if not outfit:
                st.warning(
                    "Your wardrobe does not have enough items yet. "
                    "Upload more clothes in **My Wardrobe**."
                )
            else:
                cols = st.columns(len(outfit))
                for idx, (cat, item) in enumerate(outfit.items()):
                    with cols[idx]:
                        st.image(
                            f"data/user_wardrobes/default_user/images/{item}",
                            caption=cat.capitalize(),
                            use_column_width=True
                        )

                st.markdown("### 🧠 Why this works")
                st.write(
                    f"Generated strictly from **your wardrobe**, "
                    f"optimized for **{weather} weather** and **{occasion} occasion**."
                )

        # -----------------------------
        # DATASET-CENTRIC MODE
        # -----------------------------
        else:
            outfit, reasoning = stylist_recommendation(
                gender=gender.lower(),
                weather=weather_l,
                mood=mood.lower(),
                occasion=occasion_l
            )

            image_path = generate_outfit_image(
                outfit=outfit,
                gender=gender.lower(),
                occasion=occasion_l,
                weather=weather_l
            )

            st.subheader("👕 Demo Outfit (Global Dataset)")
            if image_path:
                st.image(image_path, use_column_width=True)

            st.subheader("🧠 Stylist Reasoning")
            for r in reasoning:
                st.write("-", r)

# =================================================
# TAB 2 — TASK-2 CIR
# =================================================
with tab2:
    st.header("🧩 Complete My Outfit")

    col1, col2 = st.columns([1, 2])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload one clothing item",
            type=["jpg", "jpeg", "png"]
        )

        gender2 = st.selectbox("Gender", ["Female", "Male"], key="cir_gender")
        weather2 = st.selectbox("Weather", ["Hot", "Warm", "Cold"], key="cir_weather")
        mood2 = st.selectbox("Mood", ["Happy", "Calm", "Sad", "Angry", "Neutral"], key="cir_mood")
        occasion2 = st.selectbox("Occasion", ["Casual", "Office", "Party"], key="cir_occasion")
        category2 = st.selectbox("Uploaded Item Type", ["Top", "Pants"])

        run_cir = st.button("✨ Complete My Outfit", use_container_width=True)

    with col2:
        if run_cir and uploaded_file:
            upload_path = "temp_upload.jpg"
            with open(upload_path, "wb") as f:
                f.write(uploaded_file.read())

            st.image(upload_path, caption="Uploaded Item", width=250)

            # USER-CENTRIC CIR
            if mode == "My Wardrobe (Personalized)":
                from recommender.user_cir_engine import UserCIREngine
                engine = UserCIREngine()

                result, reason = engine.retrieve(uploaded_file.name)

                if result:
                    st.image(
                        f"data/user_wardrobes/default_user/images/{result}",
                        caption="Recommended from your wardrobe",
                        width=250
                    )
                    st.markdown("### 🧠 Why this works")
                    st.write(reason)
                else:
                    st.warning(reason)

            # DATASET-CENTRIC CIR
            else:
                from recommender.cir_engine import stylist_cir

                gender_map = {"Female": "women", "Male": "men"}
                cat_map = {"Top": "top", "Pants": "pants"}

                recs, reasons = stylist_cir(
                    upload_path,
                    cat_map[category2],
                    gender_map[gender2],
                    weather2.lower(),
                    mood2.lower(),
                    occasion2.lower()
                )

                for label, (path, score) in recs.items():
                    st.image(path, caption=f"{label} (score: {score:.2f})", width=250)

                st.markdown("### 🧠 Why this works")
                for r in reasons:
                    st.write("-", r)

# =================================================
# TAB 3 — MY WARDROBE (DIGITAL CLOSET)
# =================================================
with tab3:
    st.header("👕 My Digital Wardrobe")

    uwm = UserWardrobeManager()
    wardrobe_data = uwm.load_wardrobe()
    metadata = wardrobe_data["metadata"]

    # -------- Upload New Clothing --------
    st.subheader("➕ Add New Clothing Item")

    new_upload = st.file_uploader(
        "Upload clothing image",
        type=["jpg", "jpeg", "png"],
        key="wardrobe_upload"
    )

    if new_upload:
        temp_path = "temp_user_upload.jpg"
        with open(temp_path, "wb") as f:
            f.write(new_upload.read())

        wi = WardrobeInference()
        result = wi.analyze_image(temp_path)

        uwm.add_item(
            source_image_path=temp_path,
            item_name=new_upload.name,
            category=result["category"],
            colors=result["colors"],
            embedding=result["embedding"]
        )

        st.success("Item added to your wardrobe successfully!")
        st.rerun()

    st.divider()

    # -------- Display Wardrobe Grid --------
    st.subheader("🧺 Your Clothes")

    if not metadata:
        st.info("Your wardrobe is empty. Upload clothes to get started.")
    else:
        items = list(metadata.items())
        cols = st.columns(4)

        for idx, (item, meta) in enumerate(items):
            with cols[idx % 4]:
                st.image(
                    f"data/user_wardrobes/default_user/images/{item}",
                    use_column_width=True
                )
                st.caption(f"Category: {meta['category']}")
