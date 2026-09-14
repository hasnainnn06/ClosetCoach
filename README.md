# ClosetCoach - AI Fashion Recommender 👗👔

[![React](https://img.shields.io/badge/React-19.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-7.2-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Firebase](https://img.shields.io/badge/Firebase-Auth%20%26%20Firestore-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An intelligent, full-stack AI-driven fashion styling and wardrobe assistant. **ClosetCoach** empowers users to create curated outfits tailored to weather, mood, and occasion—either exploring vast fashion datasets or generating tailored combinations directly from their personal digital wardrobe.

---

## 🌟 Key Features

- 🎨 **Smart Outfit Generator**: Context-aware recommendation engine synthesizing color harmony, weather conditions, occasions (formal, casual, party), and mood states into complete looks.
- 🔍 **Complete Your Look (CIR)**: Composed Image Retrieval engine enabling users to upload or choose a single garment (e.g., top or trousers) and automatically retrieve stylistically matching complementary pieces.
- 👗 **Digital Wardrobe Management**: Seamlessly upload, categorize, and organize your clothing collection with cloud synchronization.
- 💾 **Saved Looks**: Bookmark and organize favorite outfit suggestions for quick access whenever you need them.
- 🚀 **Interactive Demo Mode**: Explore core AI recommendations and image retrieval without creating an account.
- 🔐 **Authentication & Cloud Storage**: Secure user authentication and real-time cloud data persistence via Firebase (Auth & Firestore).
- 📱 **Modern Responsive UI**: Built with React 19, Vite, and custom responsive CSS featuring smooth micro-animations.

---

## 🛠️ Tech Stack

| Domain | Technologies & Libraries |
|---|---|
| **Frontend** | React 19, React Router 7, Vite 7, Modern CSS, Context API |
| **Backend** | Python 3.8+, Flask, Flask-CORS, NumPy |
| **Machine Learning & Vision** | TensorFlow, OpenCV (`opencv-python`), scikit-learn, Pillow (PIL), DeepFashion dataset |
| **Cloud & Database** | Firebase Authentication, Cloud Firestore, Firebase Storage, Firebase Admin SDK |

---

## 📂 Project Structure

```text
ClosetCoach/
├── ClosetCoach-Frontend/
│   └── frontend/
│       ├── pages/               # React views (Home, Demo, OutfitGenerator, CIR, Wardrobe, SavedLooks, Login, Signup)
│       ├── src/
│       │   ├── components/      # UI components (Navbar, Footer, Cards, etc.)
│       │   ├── context/         # AuthContext & application state
│       │   ├── api.js           # REST API client
│       │   ├── firebase.js      # Firebase configuration & initialization
│       │   ├── App.jsx          # Route configurations
│       │   └── index.css        # Design tokens & styling
│       ├── .env.example         # Frontend environment template
│       ├── package.json         # Frontend dependencies & scripts
│       └── vite.config.js       # Vite build config
│
├── ClosetCoach-Backend/
│   ├── api.py                   # Flask REST API server & endpoints
│   ├── recommender/             # Stylist recommendation & visual composition logic
│   ├── wardrobe/                # User wardrobe manager & profile state
│   ├── models/                  # Neural network architectures & ML models
│   ├── data/                    # Dataset catalogs and visual embeddings
│   ├── firebase_config.py       # Firebase Admin initialization
│   └── requirements.txt         # Python dependencies
│
├── DEPLOYMENT_GUIDE.md          # Comprehensive deployment steps (Vercel & Render)
├── HOW_TO_RUN.md                # Quick local run commands
└── README.md                    # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites

- **Node.js** (v18.0.0 or higher) and **npm**
- **Python** (v3.8 or higher) and **pip**
- **Git**

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/hasnainnn06/ClosetCoach.git
cd ClosetCoach
```

---

### Step 2: Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd ClosetCoach-Backend
   ```
2. *(Optional but recommended)* Create and activate a virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   python api.py
   ```
   > 📡 Backend runs locally on **`http://localhost:5050`**

---

### Step 3: Frontend Setup

1. Open a new terminal window and navigate to the frontend app:
   ```bash
   cd ClosetCoach-Frontend/frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Configure environment variables (create a `.env` file):
   ```bash
   cp .env.example .env
   ```
   Fill in your Firebase credentials in `.env`:
   ```env
   VITE_FIREBASE_API_KEY=your_api_key
   VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=your_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   VITE_FIREBASE_APP_ID=your_app_id
   VITE_API_BASE_URL=http://localhost:5050
   ```
4. Start the frontend development server:
   ```bash
   npm run dev
   ```
   > 🌐 Application will be available at **`http://localhost:5173`**

---

## 🔌 API Reference

The backend exposes the following RESTful endpoints:

| Method | Endpoint | Description | Auth Required |
|:------:|:---------|:------------|:-------------:|
| `GET` | `/api/health` | Health check verifying API status | No |
| `POST` | `/api/generate-outfit` | Generates complete outfit recommendations from the global dataset (Demo) | No |
| `POST` | `/api/generate-outfit-user` | Generates a tailored outfit from the user's uploaded wardrobe items | Yes |
| `POST` | `/api/cir` | Composed Image Retrieval matching complementary items using uploaded garment image (Demo) | No |
| `POST` | `/api/cir-user` | Retrieves matching items from the user's personal wardrobe | Yes |

---

## 🚢 Deployment

For complete, step-by-step production deployment instructions, refer to [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md).

- **Frontend**: One-click deployment on [Vercel](https://vercel.com) using Vite preset.
- **Backend**: Containerized or Python web service on [Render](https://render.com).
- **Database / Auth**: Managed and secured via Google Firebase.

---

## 👨‍💻 Author

**Hasnain**

- GitHub: [@hasnainnn06](https://github.com/hasnainnn06)
- Email: [hasnainnn0604@gmail.com](mailto:hasnainnn0604@gmail.com)
- Repository: [ClosetCoach on GitHub](https://github.com/hasnainnn06/ClosetCoach)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [DeepFashion Dataset](http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html) for visual fashion embeddings and stylistic benchmarks.
- Google Firebase for real-time storage and authentication infrastructure.
- React and Vite open-source communities.
