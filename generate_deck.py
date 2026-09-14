import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path):
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_slide_layout = prs.slide_layouts[6]

    # Color Palette: Modern Dark Slate & Luxury Fashion Accents
    BG_COLOR = RGBColor(11, 17, 32)         # #0B1120 Deep Slate
    CARD_BG = RGBColor(23, 32, 51)          # #172033 Card Slate
    CARD_BORDER = RGBColor(45, 62, 90)      # #2D3E5A Subtle Border
    ACCENT_GOLD = RGBColor(245, 158, 11)    # #F59E0B Warm Amber / Gold
    ACCENT_CYAN = RGBColor(56, 189, 248)    # #38BDF8 Tech Cyan
    ACCENT_ROSE = RGBColor(244, 63, 94)     # #F43F5E Coral / Rose
    TEXT_WHITE = RGBColor(248, 250, 252)    # #F8FAFC Crisp White
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Slate Gray
    TEXT_LIGHT = RGBColor(203, 213, 225)    # #CBD5E1 Light Slate
    CODE_BG = RGBColor(8, 13, 24)           # #080D18 Code Editor Dark
    CODE_GREEN = RGBColor(74, 222, 128)     # #4ADE80 Code Syntax Green
    PLACEHOLDER_BG = RGBColor(20, 29, 47)   # Placeholder dark fill
    PLACEHOLDER_BORDER = RGBColor(245, 158, 11) # Highlight border

    def add_header(slide, title_text, category_badge=None):
        # Background fill
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()

        # Top decorative thin line
        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.38), Inches(11.733), Inches(0.035))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = ACCENT_GOLD
        top_line.line.fill.background()

        # Header textbox
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(11.733), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        if category_badge:
            p.text = category_badge.upper()
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN
            p.font.name = "Segoe UI"
            p_title = tf.add_paragraph()
            p_title.space_before = Pt(2)
        else:
            p_title = p

        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.font.name = "Segoe UI"

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: Project Intro
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_slide_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_COLOR
    bg1.line.fill.background()

    # Hero Banner
    add_card(slide1, Inches(0.8), Inches(0.75), Inches(11.733), Inches(2.25), bg_color=CARD_BG, border_color=ACCENT_GOLD)
    tb_hero = slide1.shapes.add_textbox(Inches(1.15), Inches(0.95), Inches(11.0), Inches(1.85))
    tf_hero = tb_hero.text_frame
    tf_hero.word_wrap = True
    
    p_badge = tf_hero.paragraphs[0]
    p_badge.text = "AI FASHION RECOMMENDER & DIGITAL WARDROBE ECOSYSTEM"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = ACCENT_GOLD
    p_badge.font.name = "Segoe UI"

    p_title = tf_hero.add_paragraph()
    p_title.space_before = Pt(4)
    p_title.text = "ClosetCoach"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.font.name = "Segoe UI"

    p_sub = tf_hero.add_paragraph()
    p_sub.space_before = Pt(6)
    p_sub.text = "An intelligent full-stack fashion platform that eliminates decision fatigue by synthesizing context-aware outfit recommendations and pairing complementary garments using deep computer vision."
    p_sub.font.size = Pt(13.5)
    p_sub.font.color.rgb = TEXT_LIGHT
    p_sub.font.name = "Segoe UI"

    # 3 Pillar Cards below hero
    pillars = [
        ("🎨 Smart Outfit Generator", 
         "Rule & ML-guided styling engine that harmonizes color psychology, weather constraints, and occasion formality to create complete outfits.",
         "• Color Theory: Mood-based harmony\n• Thermal Logic: Fabric & layering rules\n• Formality Tiers: Formal vs. Casual cuts",
         ACCENT_GOLD),
        ("🔍 Complete Your Look (CIR)", 
         "Composed Image Retrieval engine that takes any uploaded clothing item and searches visual embeddings to retrieve complementary pieces.",
         "• 128-Dim Latent Feature Vectors\n• Cosine Similarity Metric Matching\n• DeepFashion Benchmark Dataset",
         ACCENT_CYAN),
        ("👗 Cloud Personal Wardrobe", 
         "Personal digitized wardrobe manager with secure cloud persistence, in-browser image optimization, and personal lookbook storage.",
         "• Firebase Authentication & Firestore\n• Client-side HTML5 Canvas Compression\n• Saved Looks History & Management",
         ACCENT_ROSE),
    ]

    for i, (title, desc, bullets, color) in enumerate(pillars):
        x = Inches(0.8 + i * 4.0)
        add_card(slide1, x, Inches(3.3), Inches(3.733), Inches(3.6))
        tb = slide1.shapes.add_textbox(x + Inches(0.25), Inches(3.5), Inches(3.233), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16.5)
        p.font.bold = True
        p.font.color.rgb = color
        p.font.name = "Segoe UI"
        
        p_desc = tf.add_paragraph()
        p_desc.space_before = Pt(8)
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = TEXT_LIGHT
        p_desc.font.name = "Segoe UI"

        p_b = tf.add_paragraph()
        p_b.space_before = Pt(12)
        p_b.text = bullets
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = TEXT_WHITE
        p_b.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 2: Tech Stack
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide2, "Technology Stack & Technical Architecture", "SLIDE 2: TECH STACK")

    tech_cols = [
        ("Frontend Architecture", ACCENT_CYAN, [
            ("React 18 & Vite", "Component-driven Single Page Application with optimized bundler and fast HMR"),
            ("React Router 7", "Declarative client-side routing with guarded ProtectedRoute wrappers"),
            ("Context API (AuthContext)", "Real-time reactive user state management synchronized with Firebase SDK"),
            ("Modern CSS3 & Glassmorphism", "Bespoke responsive layout with CSS variables, keyframe animations & mobile support")
        ]),
        ("Backend & AI Engine", ACCENT_GOLD, [
            ("Python 3 & Flask REST API", "Lightweight backend microservice exposing 5 specialized REST endpoints"),
            ("TensorFlow & Keras", "Deep Convolutional Neural Network extracting 128-dimensional embedding vectors"),
            ("scikit-learn & NumPy", "High-performance pairwise Cosine Similarity search and KMeans color quantization"),
            ("OpenCV & Pillow (PIL)", "Image preprocessing pipeline (224x224 scaling) and dynamic vertical visualizer")
        ]),
        ("Database, Cloud & Storage", ACCENT_ROSE, [
            ("Firebase Authentication", "Secure email/password identity provider with display name profile sync"),
            ("Cloud Firestore (NoSQL)", "Real-time document database housing wardrobe collections and saved looks"),
            ("Client-Side Canvas Encoding", "In-browser Base64 JPEG downscaling (max 800px @ 70%) bypassing bucket costs"),
            ("DeepFashion Dataset", "50,000+ benchmark fashion images segmented by gender, garment type & style")
        ])
    ]

    for i, (cat_title, color, items) in enumerate(tech_cols):
        x = Inches(0.8 + i * 4.0)
        add_card(slide2, x, Inches(1.65), Inches(3.733), Inches(5.35))
        tb = slide2.shapes.add_textbox(x + Inches(0.25), Inches(1.85), Inches(3.233), Inches(4.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = cat_title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color
        p.font.name = "Segoe UI"
        
        for name, desc in items:
            pn = tf.add_paragraph()
            pn.space_before = Pt(12)
            pn.text = f"• {name}"
            pn.font.size = Pt(12.5)
            pn.font.bold = True
            pn.font.color.rgb = TEXT_WHITE
            pn.font.name = "Segoe UI"

            pd = tf.add_paragraph()
            pd.text = desc
            pd.font.size = Pt(11)
            pd.font.color.rgb = TEXT_MUTED
            pd.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 3: Project Structure
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide3, "Project Structure & Repository File Tree", "SLIDE 3: PROJECT STRUCTURE")

    # Left: Clean Code Tree Box
    add_card(slide3, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.35), bg_color=CODE_BG)
    tb_tree = slide3.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.1), Inches(4.95))
    tf_tree = tb_tree.text_frame
    tf_tree.word_wrap = True

    p = tf_tree.paragraphs[0]
    p.text = "Directory Hierarchy & Tree Structure"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD
    p.font.name = "Consolas"

    tree_str = (
        "ClosetCoach/\n"
        "├── ClosetCoach-Frontend/frontend/\n"
        "│   ├── pages/               # 9 Core Page Views\n"
        "│   │   ├── Home.jsx, Wardrobe.jsx\n"
        "│   │   ├── OutfitGenerator.jsx, CIR.jsx\n"
        "│   │   ├── Demo.jsx, SavedLooks.jsx\n"
        "│   │   └── Login.jsx, Signup.jsx, About.jsx\n"
        "│   ├── src/\n"
        "│   │   ├── App.jsx          # Protected Routes & Nav\n"
        "│   │   ├── api.js           # REST API Client\n"
        "│   │   ├── firebase.js      # Auth & Firestore Setup\n"
        "│   │   ├── context/         # AuthContext Provider\n"
        "│   │   └── components/      # Navbar, Modal, etc.\n"
        "│   └── index.html, vite.config.js\n"
        "├── ClosetCoach-Backend/\n"
        "│   ├── api.py               # Flask REST Gateway (5 Routes)\n"
        "│   ├── recommender/         # AI Recommendation Engines\n"
        "│   │   ├── stylist_engine.py       # Heuristics\n"
        "│   │   ├── cir_engine.py          # Visual Embeddings\n"
        "│   │   └── outfit_visualizer.py   # Image Composer\n"
        "│   ├── wardrobe/            # UserWardrobeManager.py\n"
        "│   ├── models/              # CNN Classifier & Weights\n"
        "│   └── data/deepfashion/    # Benchmark Dataset\n"
        "└── DEPLOYMENT_GUIDE.md, README.md"
    )
    p_tree = tf_tree.add_paragraph()
    p_tree.space_before = Pt(6)
    p_tree.text = tree_str
    p_tree.font.size = Pt(9.5)
    p_tree.font.color.rgb = CODE_GREEN
    p_tree.font.name = "Consolas"

    # Right: Architectural Breakdown
    add_card(slide3, Inches(6.6), Inches(1.65), Inches(5.933), Inches(5.35))
    tb_info = slide3.shapes.add_textbox(Inches(6.85), Inches(1.85), Inches(5.433), Inches(4.9))
    tf_info = tb_info.text_frame
    tf_info.word_wrap = True

    p = tf_info.paragraphs[0]
    p.text = "Separation of Concerns & Architecture"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.font.name = "Segoe UI"

    modules = [
        ("Presentation Layer (ClosetCoach-Frontend)",
         "Organized into routed pages and reusable UI components. Handles client-side state, Firebase Auth listeners, and asynchronous API calls."),
        ("API Gateway Layer (api.py)",
         "Exposes 5 specialized REST endpoints. Implements CORS headers, parameter parsing, and a custom NumpyJSONProvider to eliminate serialization errors."),
        ("Recommender & ML Engine (recommender/ & models/)",
         "Decouples deterministic heuristic styling (stylist_engine.py) from deep learning visual similarity (cir_engine.py) and image composition."),
        ("Persistence Layer (wardrobe/ & Firestore)",
         "Dual-tier data architecture: Cloud Firestore handles multi-user wardrobe documents, while local pickled indexes accelerate similarity queries.")
    ]

    for title, desc in modules:
        pn = tf_info.add_paragraph()
        pn.space_before = Pt(10)
        pn.text = f"• {title}"
        pn.font.size = Pt(12)
        pn.font.bold = True
        pn.font.color.rgb = TEXT_WHITE
        pn.font.name = "Segoe UI"

        pd = tf_info.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = TEXT_MUTED
        pd.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 4: ER Diagram
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide4, "Database Architecture & Entity Relationships", "SLIDE 4: ER DIAGRAM")

    # Big placeholder box on left
    add_card(slide4, Inches(0.8), Inches(1.65), Inches(7.5), Inches(5.35), bg_color=PLACEHOLDER_BG, border_color=PLACEHOLDER_BORDER)
    tb_ph = slide4.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(6.9), Inches(4.0))
    tf_ph = tb_ph.text_frame
    tf_ph.word_wrap = True
    tf_ph.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf_ph.paragraphs[0]
    p.text = "[INSERT DATABASE ER DIAGRAM IMAGE HERE]"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD
    p.font.name = "Segoe UI"

    p_sub = tf_ph.add_paragraph()
    p_sub.space_before = Pt(14)
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "High-Resolution Entity Relationship Diagram\nVisualizing Firebase Auth Users, Firestore NoSQL Collections,\nand 1-to-Many Relational Foreign Keys"
    p_sub.font.size = Pt(12.5)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.font.name = "Segoe UI"

    # Right: Firestore Collection Schema Specs
    add_card(slide4, Inches(8.5), Inches(1.65), Inches(4.033), Inches(5.35))
    tb_sc = slide4.shapes.add_textbox(Inches(8.75), Inches(1.85), Inches(3.533), Inches(4.9))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True

    p = tf_sc.paragraphs[0]
    p.text = "Firestore Entity Structure"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.font.name = "Segoe UI"

    schemas = [
        ("users (Firebase Auth)", [
            "uid: Primary Key (String)",
            "email, displayName",
            "Rel: 1-to-Many with wardrobe & savedLooks"
        ]),
        ("wardrobe (Collection)", [
            "userId: Foreign Key (Auth UID)",
            "name: Item label ('Blue Oxford Shirt')",
            "category: top | pants | jacket | dress",
            "color: blue | black | beige | etc.",
            "imageUrl: Base64 JPEG data string",
            "createdAt: ISO timestamp"
        ]),
        ("savedLooks (Collection)", [
            "userId: Foreign Key (Auth UID)",
            "type: 'outfit_generator' | 'cir'",
            "matchedItems: [{category, name, image, score}]",
            "preferences: {mood, occasion, weather}",
            "reasoning: String array",
            "savedAt: ISO timestamp"
        ])
    ]

    for title, fields in schemas:
        pn = tf_sc.add_paragraph()
        pn.space_before = Pt(10)
        pn.text = f"• {title}"
        pn.font.size = Pt(12)
        pn.font.bold = True
        pn.font.color.rgb = TEXT_WHITE
        pn.font.name = "Segoe UI"

        for f in fields:
            pf = tf_sc.add_paragraph()
            pf.text = f"   - {f}"
            pf.font.size = Pt(10)
            pf.font.color.rgb = TEXT_MUTED
            pf.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 5: Page Screenshots
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide5, "User-Flow & Core Screen Journey", "SLIDE 5: PAGE SCREENSHOTS")

    # Big placeholder box on left
    add_card(slide5, Inches(0.8), Inches(1.65), Inches(7.5), Inches(5.35), bg_color=PLACEHOLDER_BG, border_color=ACCENT_CYAN)
    tb_ph5 = slide5.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(6.9), Inches(4.0))
    tf_ph5 = tb_ph5.text_frame
    tf_ph5.word_wrap = True
    tf_ph5.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf_ph5.paragraphs[0]
    p.text = "[INSERT USER-FLOW PAGE SCREENSHOTS HERE]"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.font.name = "Segoe UI"

    p_sub5 = tf_ph5.add_paragraph()
    p_sub5.space_before = Pt(14)
    p_sub5.alignment = PP_ALIGN.CENTER
    p_sub5.text = "Complete Multi-Screen User Journey Collage:\n(1. Wardrobe Grid ➔ 2. Stepper Wizard ➔ 3. AI Result Modal ➔ 4. Saved Looks Gallery)"
    p_sub5.font.size = Pt(12.5)
    p_sub5.font.color.rgb = TEXT_MUTED
    p_sub5.font.name = "Segoe UI"

    # Right: Step highlights
    add_card(slide5, Inches(8.5), Inches(1.65), Inches(4.033), Inches(5.35))
    tb_st = slide5.shapes.add_textbox(Inches(8.75), Inches(1.85), Inches(3.533), Inches(4.9))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True

    p = tf_st.paragraphs[0]
    p.text = "Key User Touchpoints"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD
    p.font.name = "Segoe UI"

    flow_steps = [
        ("1. Digital Wardrobe Manager", "Fast image upload with client-side preview, category dropdowns, color tags, and responsive item deletion."),
        ("2. Interactive Stepper Wizard", "Step-by-step preference selector covering Mood (Casual/Confident), Occasion (Office/Party), and Weather (Hot/Cold)."),
        ("3. Outfit Recommendation Modal", "Visual composite display pairing matched items alongside transparent stylist reasoning and instant lookbook saving."),
        ("4. Complete Your Look (CIR)", "Interactive drag-and-drop tool discovering matching bottoms or layers for any uploaded standalone piece."),
        ("5. Saved Looks Portfolio", "Comprehensive visual history of favorited outfits with metadata tags and timestamped styling details.")
    ]

    for title, desc in flow_steps:
        pn = tf_st.add_paragraph()
        pn.space_before = Pt(8)
        pn.text = f"• {title}"
        pn.font.size = Pt(11.5)
        pn.font.bold = True
        pn.font.color.rgb = TEXT_WHITE
        pn.font.name = "Segoe UI"

        pd = tf_st.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = TEXT_MUTED
        pd.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 6: New Features You Added (HEAVY FOCUS)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide6, "Uniquely Engineered Custom Features", "SLIDE 6: NEW FEATURES ADDED (HEAVY FOCUS)")

    # 4 distinct custom features across 2 left columns
    features = [
        ("1. Dual-Mode Recommender System",
         "Solves the user onboarding dilemma by supporting two operating tiers:\n"
         "• Demo Mode: Queries 50k+ DeepFashion items with zero sign-up friction.\n"
         "• User Mode: Reads Firebase Firestore to curate looks strictly from user-owned garments.",
         ACCENT_GOLD),
        ("2. Multi-Factor Contextual Stylist Engine",
         "Harmonizes 4 independent fashion dimensions into coherent outfits:\n"
         "• Mood ➔ Color Psychology: Maps moods to harmonic color palettes.\n"
         "• Weather ➔ Thermal Logic: Enforces fabric & seasonal layering.\n"
         "• Occasion ➔ Formality: Strict formal vs. casual garment cuts.",
         ACCENT_CYAN),
        ("3. Composed Image Retrieval (CIR)",
         "Advanced complementary matching beyond standard visual similarity:\n"
         "• Detects uploaded category (e.g. Pants) & infers missing piece (Top).\n"
         "• Formulates cosine similarity queries over filtered visual embeddings.\n"
         "• Recommends coordinated pieces with real-time confidence scores.",
         ACCENT_ROSE),
        ("4. Client-Side Image Optimization Pipeline",
         "Bypasses expensive cloud bucket storage & slow network transfers:\n"
         "• In-browser HTML5 Canvas downsampling (max 800px dimension).\n"
         "• 70% quality JPEG compression direct-to-Base64 in memory.\n"
         "• Stores lightweight Base64 payloads directly in Firestore documents.",
         TEXT_WHITE)
    ]

    col_w = Inches(3.733)
    card_h = Inches(2.55)
    for i, (title, desc, color) in enumerate(features):
        row = i // 2
        col = i % 2
        x = Inches(0.8 + col * 4.0)
        y = Inches(1.65 + row * 2.75)
        
        add_card(slide6, x, y, col_w, card_h)
        tb = slide6.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), col_w - Inches(0.4), card_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = color
        p.font.name = "Segoe UI"

        pd = tf.add_paragraph()
        pd.space_before = Pt(6)
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = TEXT_LIGHT
        pd.font.name = "Segoe UI"

    # Right side: Prominent placeholders for UI & Backend screenshots
    add_card(slide6, Inches(8.8), Inches(1.65), Inches(3.733), Inches(2.55), bg_color=PLACEHOLDER_BG, border_color=ACCENT_GOLD)
    tb_p1 = slide6.shapes.add_textbox(Inches(8.95), Inches(1.85), Inches(3.433), Inches(2.15))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True
    tf_p1.vertical_anchor = MSO_ANCHOR.MIDDLE

    p1 = tf_p1.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "[INSERT FEATURE SCREENSHOT: OUTFIT GENERATOR & STYLIST REASONING MODAL]"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_GOLD
    p1.font.name = "Segoe UI"

    add_card(slide6, Inches(8.8), Inches(4.4), Inches(3.733), Inches(2.6), bg_color=PLACEHOLDER_BG, border_color=ACCENT_CYAN)
    tb_p2 = slide6.shapes.add_textbox(Inches(8.95), Inches(4.6), Inches(3.433), Inches(2.2))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True
    tf_p2.vertical_anchor = MSO_ANCHOR.MIDDLE

    p2 = tf_p2.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "[INSERT BACKEND SCREENSHOT: CIR API & COMPLEMENTARY MATCH OUTPUT]"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_CYAN
    p2.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 7: Important Algorithms (HEAVY FOCUS)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide7, "Core Algorithmic Logic & Mathematical Formulations", "SLIDE 7: IMPORTANT ALGORITHMS (HEAVY FOCUS)")

    # Left Column: CIR Cosine Similarity Retrieval
    add_card(slide7, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.35))
    
    # Left Header
    tb_h1 = slide7.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.3), Inches(0.9))
    tf_h1 = tb_h1.text_frame
    tf_h1.word_wrap = True
    p = tf_h1.paragraphs[0]
    p.text = "1. Category-Constrained CIR Embedding Retrieval"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.font.name = "Segoe UI"

    p_sub1 = tf_h1.add_paragraph()
    p_sub1.space_before = Pt(3)
    p_sub1.text = "Extracts 128-d latent CNN vectors, L2-normalizes, and computes cosine similarity across category-filtered candidate partitions:"
    p_sub1.font.size = Pt(10.5)
    p_sub1.font.color.rgb = TEXT_MUTED
    p_sub1.font.name = "Segoe UI"

    # Left Code Box
    add_card(slide7, Inches(1.0), Inches(2.75), Inches(5.3), Inches(2.75), bg_color=CODE_BG)
    tb_c1 = slide7.shapes.add_textbox(Inches(1.1), Inches(2.82), Inches(5.1), Inches(2.6))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    
    code1 = (
        "# recommender/cir_engine.py\n"
        "def retrieve_similar(query_img, gender, category, top_k=1):\n"
        "    query_emb = extract_embedding(query_img)  # 128-dim\n"
        "    candidates = [it for it in get_embedding_index()\n"
        "                  if it['gender'] == gender and it['category'] == category]\n"
        "    scored = []\n"
        "    for item in candidates:\n"
        "        # Cosine Similarity: (u . v) / (||u|| * ||v||)\n"
        "        sim = cosine_similarity([query_emb], [item['embedding']])[0][0]\n"
        "        scored.append((item['path'], float(sim)))\n"
        "    scored.sort(key=lambda x: x[1], reverse=True)\n"
        "    return scored[:top_k]"
    )
    p_c1 = tf_c1.paragraphs[0]
    p_c1.text = code1
    p_c1.font.size = Pt(9.0)
    p_c1.font.color.rgb = CODE_GREEN
    p_c1.font.name = "Consolas"

    # Left Footer Takeaways
    tb_f1 = slide7.shapes.add_textbox(Inches(1.0), Inches(5.58), Inches(5.3), Inches(1.3))
    tf_f1 = tb_f1.text_frame
    tf_f1.word_wrap = True
    p_t1 = tf_f1.paragraphs[0]
    p_t1.text = "• Solves visual harmony while strictly adhering to category & formality boundaries.\n• Pre-normalizing embedding vectors guarantees strict [-1.0, 1.0] scoring bounds."
    p_t1.font.size = Pt(10.5)
    p_t1.font.color.rgb = TEXT_WHITE
    p_t1.font.name = "Segoe UI"

    # Right Column: Multi-Factor Heuristic Scoring Engine
    add_card(slide7, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.35))

    # Right Header
    tb_h2 = slide7.shapes.add_textbox(Inches(7.0), Inches(1.75), Inches(5.333), Inches(0.9))
    tf_h2 = tb_h2.text_frame
    tf_h2.word_wrap = True
    p2 = tf_h2.paragraphs[0]
    p2.text = "2. Multi-Factor User Wardrobe Scoring Engine"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_GOLD
    p2.font.name = "Segoe UI"

    p_sub2 = tf_h2.add_paragraph()
    p_sub2.space_before = Pt(3)
    p_sub2.text = "Scores user-owned garments using mood-color psychology, neutral versatility bonuses, thermal weather rules, and controlled randomness:"
    p_sub2.font.size = Pt(10.5)
    p_sub2.font.color.rgb = TEXT_MUTED
    p_sub2.font.name = "Segoe UI"

    # Right Code Box
    add_card(slide7, Inches(7.0), Inches(2.75), Inches(5.333), Inches(2.75), bg_color=CODE_BG)
    tb_c2 = slide7.shapes.add_textbox(Inches(7.1), Inches(2.82), Inches(5.133), Inches(2.6))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True

    code2 = (
        "# api.py (generate_outfit_user route)\n"
        "for cat in required_categories:\n"
        "    scored = []\n"
        "    for item in items_by_category[cat]:\n"
        "        score = 0.5  # Base affinity\n"
        "        item_color = (item.get('color') or '').lower()\n"
        "        if item_color in preferred_colors: score += 0.30\n"
        "        if item_color in ['black','white','gray','beige']:\n"
        "            score += 0.10  # Neutral color versatility bonus\n"
        "        score += random.random() * 0.10  # Stochastic variety\n"
        "        scored.append((item, score))\n"
        "    outfit[cat] = sorted(scored, key=lambda x: x[1], reverse=True)[0][0]"
    )
    p_c2 = tf_c2.paragraphs[0]
    p_c2.text = code2
    p_c2.font.size = Pt(9.0)
    p_c2.font.color.rgb = CODE_GREEN
    p_c2.font.name = "Consolas"

    # Right Footer Takeaways
    tb_f2 = slide7.shapes.add_textbox(Inches(7.0), Inches(5.58), Inches(5.333), Inches(1.3))
    tf_f2 = tb_f2.text_frame
    tf_f2.word_wrap = True
    p_t2 = tf_f2.paragraphs[0]
    p_t2.text = "• Eliminates static deterministic repetition, generating fresh looks upon every re-roll.\n• Bridges subjective human fashion styling rules with algorithmic ranking."
    p_t2.font.size = Pt(10.5)
    p_t2.font.color.rgb = TEXT_WHITE
    p_t2.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 8: Major Challenge Faced (HEAVY FOCUS)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide8, "Major Technical Challenges Encountered & Architectural Solutions", "SLIDE 8: MAJOR CHALLENGES FACED (HEAVY FOCUS)")

    # Prominent Header Banner
    add_card(slide8, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.85), bg_color=CARD_BG, border_color=ACCENT_ROSE)
    tb_pr = slide8.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.333), Inches(0.75))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True
    tf_pr.vertical_anchor = MSO_ANCHOR.MIDDLE

    p_pr = tf_pr.paragraphs[0]
    p_pr.text = "[INSERT THE BIGGEST CHALLENGE HIT AND HOW WE SOLVED IT]"
    p_pr.alignment = PP_ALIGN.CENTER
    p_pr.font.size = Pt(16.5)
    p_pr.font.bold = True
    p_pr.font.color.rgb = ACCENT_ROSE
    p_pr.font.name = "Segoe UI"

    # 3 Distinct Technical Challenges Faced & Solved
    challenges = [
        ("1. ML Latency & Server Reload Locks", ACCENT_GOLD,
         "CHALLENGE:\n"
         "Compiling TensorFlow model graphs on incoming requests induced 4-6 second latency bottlenecks. Furthermore, Flask's watchdog file reloader conflicted with TF's file monitoring threads, deadlocking the server.\n\n"
         "HOW WE SOLVED IT:\n"
         "• Implemented a Lazy-Loading Singleton Pattern (`get_model()`) to load and pin model weights in memory on initial demand.\n"
         "• Generated pre-computed embedding pickle indexes (`embedding_index.pkl`) for sub-second candidate retrieval.\n"
         "• Explicitly disabled `use_reloader=False` in API production startup."),
        
        ("2. NumPy Serialization Incompatibility", ACCENT_CYAN,
         "CHALLENGE:\n"
         "Vector similarity outputs produced `np.float32`, `np.integer`, and `np.ndarray` objects. Flask's standard `jsonify` threw `TypeError: Object of type float32 is not JSON serializable`.\n\n"
         "HOW WE SOLVED IT:\n"
         "• Subclassed Flask 2.2+'s `DefaultJSONProvider` to engineer a custom `NumpyJSONProvider`.\n"
         "• Intercepted all NumPy primitives, auto-casting them to native Python floats, ints, and lists before response serialization.\n"
         "• Guaranteed bulletproof serialization across all ML endpoints."),
        
        ("3. Cloud Storage Costs & Upload Latency", ACCENT_ROSE,
         "CHALLENGE:\n"
         "Uploading raw multi-megabyte mobile photos directly to cloud storage buckets introduced network latency, exceeded free storage quotas, and triggered CORS configuration issues.\n\n"
         "HOW WE SOLVED IT:\n"
         "• Developed a client-side HTML5 Canvas compressor in `Wardrobe.jsx`.\n"
         "• Automatically downsamples images to a maximum 800px dimension and re-encodes as 70% quality JPEG Base64.\n"
         "• Stored optimized Base64 payloads directly in Firestore documents, cutting payload sizes by >85% and eliminating cloud bucket fees.")
    ]

    for i, (title, color, body) in enumerate(challenges):
        x = Inches(0.8 + i * 4.0)
        add_card(slide8, x, Inches(2.52), Inches(3.733), Inches(4.55))
        tb = slide8.shapes.add_textbox(x + Inches(0.2), Inches(2.65), Inches(3.333), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = color
        p.font.name = "Segoe UI"

        pb = tf.add_paragraph()
        pb.space_before = Pt(8)
        pb.text = body
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = TEXT_LIGHT
        pb.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 9: What You'll Add Next
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide9, "Future Roadmap & Planned Next-Gen Innovations", "SLIDE 9: WHAT YOU'LL ADD NEXT")

    next_features = [
        ("1. Automatic Garment Tagging via Vision",
         "Eliminate manual color and category inputs during wardrobe cataloging:\n\n"
         "• Deploy a lightweight MobileNetV3 / YOLOv8 clothing classification model.\n"
         "• Perform instantaneous on-device inference to classify category (Top, Pants, Outerwear, Footwear).\n"
         "• Integrate OpenCV KMeans clustering to extract exact HEX/RGB dominant color palettes automatically upon image drop.",
         ACCENT_CYAN),
        ("2. Hyperlocal Real-Time Weather Integration",
         "Transition weather inputs from manual selection to ambient contextual intelligence:\n\n"
         "• Connect to OpenWeatherMap / WeatherAPI using browser Geolocation coordinates.\n"
         "• Extract real-time temperature, humidity, precipitation probability, and wind chill.\n"
         "• Automatically apply thermal fabric constraints (e.g. recommending water-resistant shells on rainy days without manual input).",
         ACCENT_GOLD),
        ("3. Generative Virtual Try-On (VTON) & 3D Avatars",
         "Advance from 2D flat composition to personalized photorealistic visualization:\n\n"
         "• Incorporate diffusion-based Virtual Try-On networks (such as IDM-VTON or TryOnDiffusion).\n"
         "• Warp selected wardrobe garments onto a user avatar or upload selfie to showcase exact fit, draping, and proportions.\n"
         "• Allow users to preview entire coordinated lookbooks dynamically before dressing.",
         ACCENT_ROSE)
    ]

    for i, (title, body, color) in enumerate(next_features):
        x = Inches(0.8 + i * 4.0)
        add_card(slide9, x, Inches(1.65), Inches(3.733), Inches(5.35))
        tb = slide9.shapes.add_textbox(x + Inches(0.25), Inches(1.85), Inches(3.233), Inches(4.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        p.font.name = "Segoe UI"

        pb = tf.add_paragraph()
        pb.space_before = Pt(12)
        pb.text = body
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = TEXT_LIGHT
        pb.font.name = "Segoe UI"

    prs.save(output_path)
    print(f"Refined presentation successfully saved to {output_path}")

if __name__ == "__main__":
    out_file = os.path.abspath("ClosetCoach_Presentation.pptx")
    create_presentation(out_file)
