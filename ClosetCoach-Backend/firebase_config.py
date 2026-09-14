# Firebase Admin SDK Configuration for ClosetCoach Backend
# This module provides Firestore access to user wardrobe data

import firebase_admin
from firebase_admin import credentials, firestore
import os

# -------------------------------------------------
# Initialize Firebase Admin SDK
# -------------------------------------------------
_firebase_app = None
_firestore_client = None

def get_firestore_client():
    """
    Get Firestore client (lazy initialization)
    Uses service account if available, otherwise uses application default credentials
    """
    global _firebase_app, _firestore_client
    
    if _firestore_client is not None:
        return _firestore_client
    
    try:
        # Try to use service account if exists
        service_account_path = os.path.join(os.path.dirname(__file__), "firebase-service-account.json")
        
        if os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            _firebase_app = firebase_admin.initialize_app(cred)
        else:
            # Use application default credentials (for local development)
            # This requires GOOGLE_APPLICATION_CREDENTIALS env var or gcloud auth
            _firebase_app = firebase_admin.initialize_app()
        
        _firestore_client = firestore.client()
        return _firestore_client
        
    except Exception as e:
        print(f"Warning: Could not initialize Firebase Admin - {e}")
        return None


def get_user_wardrobe(user_id):
    """
    Fetch user's wardrobe items from Firestore
    
    Args:
        user_id: Firebase user UID
        
    Returns:
        List of wardrobe items with their metadata and image URLs
    """
    try:
        db = get_firestore_client()
        if db is None:
            return []
        
        # Query wardrobe collection for this user
        wardrobe_ref = db.collection('wardrobe')
        query = wardrobe_ref.where('userId', '==', user_id)
        
        items = []
        for doc in query.stream():
            item = doc.to_dict()
            item['id'] = doc.id
            items.append(item)
        
        return items
        
    except Exception as e:
        print(f"Error fetching wardrobe: {e}")
        return []


def get_items_by_category(user_id, category):
    """
    Get wardrobe items filtered by category
    
    Args:
        user_id: Firebase user UID
        category: Category like 'top', 'pants', 'jacket'
        
    Returns:
        List of items matching the category
    """
    items = get_user_wardrobe(user_id)
    return [item for item in items if item.get('category') == category]
