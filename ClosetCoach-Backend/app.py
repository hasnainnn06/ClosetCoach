import streamlit as st

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="ClosetCoach",
    layout="wide"
)

# ------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# ------------------------------------------------------
# GLOBAL CSS (THIS IS THE KEY PART)
# ------------------------------------------------------
st.markdown("""
<style>

/* Hide Streamlit default UI */
#MainMenu, footer, header {visibility: hidden;}

/* App background */
body {
    background-color: #f5f6fb;
}

/* Container padding */
.block-container {
    padding: 1.5rem 4rem;
    max-width: 1400px;
}

/* Header */
.cc-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}
.cc-title {
    font-size: 30px;
    font-weight: 700;
}
.cc-gear {
    font-size: 22px;
}

/* Hero */
.hero {
    position: relative;
    height: 300px;
    border-radius: 22px;
    overflow: hidden;
    margin-bottom: 24px;
}
.hero img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.55), transparent);
}
.hero-text {
    position: absolute;
    bottom: 24px;
    left: 28px;
    color: white;
}
.hero-text h2 {
    margin: 0;
    font-size: 28px;
}
.hero-text p {
    margin-top: 6px;
    font-size: 15px;
}

/* Controls */
.controls {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
}
.upload-box, .mood-box {
    flex: 1;
    background: white;
    padding: 14px;
    border-radius: 16px;
    text-align: center;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

/* Weather box */
.weather-box {
    background: #eef0ff;
    padding: 14px 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    font-size: 15px;
}

/* CTA Button */
.cta-btn {
    width: 100%;
    background: #4f46e5;
    color: white;
    border: none;
    padding: 16px;
    border-radius: 18px;
    font-size: 16px;
    font-weight: 700;
    margin-top: 10px;
}

/* Cards */
.card {
    background: white;
    border-radius: 20px;
    padding: 14px;
    margin-bottom: 18px;
    display: flex;
    gap: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
.card img {
    width: 120px;
    border-radius: 16px;
}
.card-meta {
    font-size: 13px;
    color: #6b7280;
}
.card-title {
    font-size: 17px;
    font-weight: 700;
    margin-top: 4px;
}
.card-desc {
    font-size: 14px;
    color: #374151;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# HEADER
# ------------------------------------------------------
st.markdown("""
<div class="cc-header">
    <div class="cc-title">ClosetCoach</div>
    <div class="cc-gear">⚙️</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# HERO
# ------------------------------------------------------
st.markdown("""
<div class="hero">
    <img src="https://images.unsplash.com/photo-1521334884684-d80222895322">
    <div class="hero-overlay"></div>
    <div class="hero-text">
        <h2>ClosetCoach – Your Smart Fashion Advisor</h2>
        <p>Upload your wardrobe, set your mood, and let AI style your day!</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# INPUT CONTROLS (VISUAL)
# ------------------------------------------------------
st.markdown("""
<div class="controls">
    <div class="upload-box">⬆ Upload Clothes</div>
    <div class="mood-box">😊 Happy</div>
</div>
""", unsafe_allow_html=True)

# REAL STREAMLIT INPUTS (HIDDEN FUNCTIONALITY)
uploaded_files = st.file_uploader(
    "Upload",
    accept_multiple_files=True,
    label_visibility="collapsed"
)

mood = st.selectbox(
    "Mood",
    ["Happy", "Casual", "Formal", "Party"],
    label_visibility="collapsed"
)

# ------------------------------------------------------
# WEATHER + OCCASION
# ------------------------------------------------------
st.markdown('<div class="weather-box">🌤️ Sunny, 24°C</div>', unsafe_allow_html=True)

occasion = st.text_input(
    "Occasion",
    placeholder="e.g., Brunch with friends"
)

# ------------------------------------------------------
# CTA BUTTON
# ------------------------------------------------------
if st.button("Get Recommendations"):
    st.session_state.show_results = True

# ------------------------------------------------------
# OUTPUT
# ------------------------------------------------------
if st.session_state.show_results:

    st.subheader("Outfit Recommendations")

    recommendations = [
        {
            "img": "https://assets.myntassets.com/images/16417668/2022/2/14/White-Tee.jpg",
            "title": "White Tee & Denim Shorts",
            "meta": "Mood: Casual · Weather: Sunny",
            "desc": "A classic, comfortable look for a sunny day."
        },
        {
            "img": "https://assets.myntassets.com/images/16613202/2022/1/5/Linen-Shirt.jpg",
            "title": "Linen Shirt & Chinos",
            "meta": "Mood: Casual · Weather: Sunny",
            "desc": "A breathable and stylish choice for warm weather."
        }
    ]

    for rec in recommendations:
        st.markdown(f"""
        <div class="card">
            <img src="{rec['img']}">
            <div>
                <div class="card-meta">{rec['meta']}</div>
                <div class="card-title">{rec['title']}</div>
                <div class="card-desc">{rec['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
