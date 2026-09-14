# ClosetCoach - AI Fashion Recommender 👗👔

An AI-powered fashion recommendation system that helps users generate complete outfits and find matching clothing items from their personal wardrobe.

![ClosetCoach Banner](https://img.shields.io/badge/ClosetCoach-AI%20Fashion-FFD700?style=for-the-badge)

## ✨ Features

- **🎨 Outfit Generator** - Generate complete outfit suggestions based on mood, occasion, and weather
- **🔍 Complete Your Look (CIR)** - Upload one piece and find matching items from your wardrobe
- **👗 Personal Wardrobe** - Upload and manage your clothing items with Firebase storage
- **🔐 User Authentication** - Secure login/signup with Firebase Auth
- **📱 Responsive Design** - Beautiful UI that works on all devices

---

## 🛠️ Tech Stack

### Frontend
- React 18 + Vite
- Firebase (Auth + Firestore)
- Modern CSS with animations

### Backend
- Python 3.x
- Flask + Flask-CORS
- TensorFlow (for AI models)

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/shariq8055/ClosetCoach.git
cd ClosetCoach
```

### Step 2: Install Frontend Dependencies
```bash
cd Final-AI/frontend
npm install
```

### Step 3: Install Backend Dependencies
```bash
cd ../../ClosetCoach-Backend
pip install flask flask-cors
```

### Step 4: Run the Application

**Open two terminal windows:**

**Terminal 1 - Frontend:**
```bash
cd Final-AI/frontend
npm run dev
```
Frontend runs on: http://localhost:5173

**Terminal 2 - Backend:**
```bash
cd ClosetCoach-Backend
python api.py
```
Backend runs on: http://localhost:5050

### Step 5: Open in Browser
Navigate to **http://localhost:5173**

---

## 📂 Project Structure

```
ClosetCoach/
├── Final-AI/
│   └── frontend/          # React frontend
│       ├── pages/         # Page components
│       ├── src/           # Source files
│       │   ├── context/   # Auth context
│       │   ├── firebase.js# Firebase config
│       │   └── api.js     # API utilities
│       └── index.html
│
├── ClosetCoach-Backend/   # Python backend
│   ├── api.py             # Flask API server
│   ├── recommender/       # AI recommendation engines
│   ├── wardrobe/          # Wardrobe management
│   └── models/            # ML models
│
└── README.md
```

---

## 🔧 Configuration

### Firebase Setup
The app uses Firebase for authentication and data storage. The configuration is in:
- `Final-AI/frontend/src/firebase.js`

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/generate-outfit` | POST | Generate outfit from dataset |
| `/api/generate-outfit-user` | POST | Generate from user wardrobe |
| `/api/cir` | POST | Complete outfit (CIR) |

---

## 📱 Screenshots

### Outfit Generator
Generate complete outfit suggestions by selecting mood, occasion, and weather.

### Complete Your Look
Upload a clothing item and get matching pieces from your wardrobe.

### My Wardrobe
Manage your personal clothing collection.

---

## 👨‍💻 Author

**Shariq** - [GitHub](https://github.com/shariq8055)

---

## 📄 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- DeepFashion Dataset
- Firebase
- React + Vite
