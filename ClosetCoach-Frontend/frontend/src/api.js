/**
 * API utility for ClosetCoach frontend
 * Handles all communication with the Python ML backend
 */

const API_BASE = 'http://localhost:5050';

/**
 * Generate outfit from dataset (Demo mode - no login required)
 */
export async function generateOutfitDemo({ gender, mood, occasion, weather }) {
    try {
        const response = await fetch(`${API_BASE}/api/generate-outfit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ gender, mood, occasion, weather }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error generating outfit:', error);
        return {
            success: false,
            error: error.message || 'Failed to connect to server'
        };
    }
}

/**
 * Generate outfit from user's wardrobe (requires login)
 * Sends wardrobe items from Firebase to backend for selection
 */
export async function generateOutfitUser({ userId, mood, occasion, weather, wardrobeItems }) {
    try {
        const response = await fetch(`${API_BASE}/api/generate-outfit-user`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId, mood, occasion, weather, wardrobeItems }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error generating user outfit:', error);
        return {
            success: false,
            error: error.message || 'Failed to connect to server'
        };
    }
}

/**
 * Complete outfit using CIR from dataset (Demo mode)
 */
export async function completeOutfitDemo({ imageFile, gender, category, mood, occasion, weather }) {
    try {
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('gender', gender);
        formData.append('category', category);
        formData.append('mood', mood);
        formData.append('occasion', occasion);
        formData.append('weather', weather);

        // Add timeout for CIR requests (120 seconds - AI processing can be slow on first load)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 120000);

        const response = await fetch(`${API_BASE}/api/cir`, {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error completing outfit:', error);
        if (error.name === 'AbortError') {
            return {
                success: false,
                error: 'Request timed out. The AI model is taking too long to process.'
            };
        }
        return {
            success: false,
            error: error.message || 'Failed to connect to server'
        };
    }
}

/**
 * Complete outfit using CIR from user's wardrobe (requires login)
 */
export async function completeOutfitUser({ userId, itemName }) {
    try {
        const response = await fetch(`${API_BASE}/api/cir-user`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId, itemName }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error completing user outfit:', error);
        return {
            success: false,
            error: error.message || 'Failed to connect to server'
        };
    }
}

/**
 * Check if the ML backend is running
 */
export async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        return response.ok;
    } catch {
        return false;
    }
}
