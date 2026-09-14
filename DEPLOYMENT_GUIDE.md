# ClosetCoach Deployment Guide

Deploy your ClosetCoach project online using free hosting services.

---

## Prerequisites

Before deploying, ensure you have:
- [ ] GitHub account (create at github.com)
- [ ] Your project pushed to a GitHub repository
- [ ] All environment variables documented

---

## Part 1: Push to GitHub

```bash
# In your project root folder
cd c:\Users\admin\Desktop\closetcoach

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - ClosetCoach"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/closetcoach.git
git branch -M main
git push -u origin main
```

---

## Part 2: Deploy Frontend (Vercel - Recommended)

### Step 1: Sign up
Go to [vercel.com](https://vercel.com) and sign up with GitHub

### Step 2: Import Project
1. Click **"Add New..."** → **"Project"**
2. Select your **closetcoach** repository
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `ClosetCoach-Frontend/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 3: Add Environment Variables
In Vercel project settings → Environment Variables, add:

| Variable | Value |
|----------|-------|
| `VITE_FIREBASE_API_KEY` | Your Firebase API key |
| `VITE_FIREBASE_AUTH_DOMAIN` | your-project.firebaseapp.com |
| `VITE_FIREBASE_PROJECT_ID` | your-project-id |
| `VITE_FIREBASE_STORAGE_BUCKET` | your-project.appspot.com |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Your sender ID |
| `VITE_FIREBASE_APP_ID` | Your app ID |
| `VITE_API_BASE_URL` | Your backend URL (add after deploying backend) |

### Step 4: Deploy
Click **"Deploy"** - Your site will be live at `https://your-project.vercel.app`

---

## Part 3: Deploy Python Backend (Render - Recommended)

### Step 1: Sign up
Go to [render.com](https://render.com) and sign up with GitHub

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repo
3. Configure:
   - **Name**: closetcoach-backend
   - **Root Directory**: `ClosetCoach-Backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

### Step 3: Add requirements.txt
Make sure `ClosetCoach-Backend/requirements.txt` exists with:
```
fastapi
uvicorn
python-multipart
tensorflow
numpy
pillow
opencv-python-headless
```

### Step 4: Deploy
Click **"Create Web Service"** - Backend will be live at `https://closetcoach-backend.onrender.com`

### Step 5: Update Frontend
Go back to Vercel and update `VITE_API_BASE_URL` to your Render backend URL.

---

## Part 4: Update Firebase Security Rules

In Firebase Console → Firestore → Rules, ensure:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /wardrobe/{document} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
      allow create: if request.auth != null;
    }
    match /savedLooks/{document} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
      allow create: if request.auth != null;
    }
  }
}
```

---

## Part 5: Add Authorized Domains

In Firebase Console → Authentication → Settings → Authorized domains:
- Add your Vercel domain: `your-project.vercel.app`

---

## 🎉 Done!

Your ClosetCoach is now live:
- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://closetcoach-backend.onrender.com`

### Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Add frontend URL to backend CORS settings |
| Auth not working | Add domain to Firebase authorized domains |
| Images not loading | Check Firebase Storage rules |
| Backend timeout | Render free tier sleeps after 15min inactivity |

---

## Alternative: Firebase Hosting (Optional)

If you prefer Firebase Hosting for frontend:

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize hosting
cd ClosetCoach-Frontend/frontend
firebase init hosting

# Build the app
npm run build

# Deploy
firebase deploy --only hosting
```

Your site will be at: `https://your-project.web.app`
