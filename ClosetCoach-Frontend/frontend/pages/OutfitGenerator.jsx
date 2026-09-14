import { useState, useEffect } from "react";
import Modal from "../src/components/Modal";
import { useAuth } from "../src/context/AuthContext";
import { generateOutfitUser } from "../src/api";
import { db } from "../src/firebase";
import { collection, getDocs, query, where, addDoc } from "firebase/firestore";

const OutfitGenerator = () => {
  const { user } = useAuth();
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({
    mood: "",
    occasion: "",
    weather: ""
  });
  const [isLoading, setIsLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [wardrobeItems, setWardrobeItems] = useState([]);
  const [wardrobeLoading, setWardrobeLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Fetch user's wardrobe on mount
  useEffect(() => {
    if (user) {
      fetchWardrobe();
    }
  }, [user]);

  const fetchWardrobe = async () => {
    setWardrobeLoading(true);
    try {
      const q = query(
        collection(db, "wardrobe"),
        where("userId", "==", user.uid)
      );
      const querySnapshot = await getDocs(q);
      const items = [];
      querySnapshot.forEach((doc) => {
        items.push({ id: doc.id, ...doc.data() });
      });
      setWardrobeItems(items);
    } catch (err) {
      console.error("Failed to fetch wardrobe:", err);
    } finally {
      setWardrobeLoading(false);
    }
  };

  const nextStep = () => setStep(prev => prev + 1);
  const prevStep = () => setStep(prev => prev - 1);

  const handleChange = (key, value) => {
    setFormData({ ...formData, [key]: value });
  };

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);

    // Check if wardrobe has items
    if (wardrobeItems.length === 0) {
      setError("Your wardrobe is empty. Please upload some clothes first.");
      setIsLoading(false);
      return;
    }

    try {
      const response = await generateOutfitUser({
        userId: user?.uid || "default_user",
        mood: formData.mood,
        occasion: formData.occasion,
        weather: formData.weather,
        wardrobeItems: wardrobeItems  // Send wardrobe items to backend
      });

      if (response.success) {
        setResult(response);
        setShowResult(true);
      } else {
        setError(response.error || "Failed to generate outfit");
      }
    } catch (err) {
      setError("Could not connect to the ML server. Please make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const resetGenerator = () => {
    setStep(0);
    setFormData({ mood: "", occasion: "", weather: "" });
    setShowResult(false);
    setResult(null);
    setError(null);
    setSaveSuccess(false);
  };

  const handleSaveLook = async () => {
    if (!user || !result) return;

    setIsSaving(true);
    setError(null);

    try {
      // Build matched items array from result
      const matchedItems = [];
      if (result.outfitImages) {
        Object.entries(result.outfitImages).forEach(([category, imageUrl]) => {
          if (imageUrl) {
            matchedItems.push({
              category: category,
              imageBase64: imageUrl,
              name: result.outfit?.[category] || category,
              score: 0.9
            });
          }
        });
      }

      const savedLook = {
        userId: user.uid,
        type: "outfit_generator",
        uploadedItem: null, // No uploaded item for outfit generator
        matchedItems: matchedItems,
        preferences: {
          mood: formData.mood,
          occasion: formData.occasion,
          weather: formData.weather
        },
        reasoning: result.reasoning || [],
        savedAt: new Date().toISOString()
      };

      await addDoc(collection(db, "savedLooks"), savedLook);

      setSaveSuccess(true);
      setTimeout(() => {
        setShowResult(false);
        resetGenerator();
      }, 1500);
    } catch (err) {
      console.error("Failed to save look:", err);
      setError("Failed to save this look. Please try again.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <main className="cc-outfit-page">
      {/* =========================
         PAGE HEADER
         ========================= */}
      <section className="cc-outfit-header">
        <span className="cc-section-tag">AI-Powered Styling</span>
        <h1>Outfit Generator</h1>
        <p>
          Answer a few quick questions and let ClosetCoach create the perfect
          outfit from your personal wardrobe. No more outfit anxiety!
        </p>
      </section>

      {/* Progress Indicator */}
      {step > 0 && step < 4 && (
        <div className="cc-progress-container">
          <div className="cc-progress-bar">
            <div
              className="cc-progress-fill"
              style={{ width: `${(step / 3) * 100}%` }}
            ></div>
          </div>
          <span className="cc-progress-text">Step {step} of 3</span>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="cc-error-message">
          <span>⚠️</span> {error}
        </div>
      )}

      {/* =========================
         STEP 0 – START
         ========================= */}
      {step === 0 && (
        <div className="cc-step-card slide-in">
          <div className="cc-step-icon-box">
            <div className="cc-icon-sparkle"></div>
          </div>
          <h3>Ready to Look Amazing?</h3>
          <p>
            We'll ask you 3 simple questions about your mood, occasion, and
            weather. Then our AI will work its magic on your wardrobe!
          </p>
          <div className="cc-step-features">
            <span>Takes 30 seconds</span>
            <span>Personalized results</span>
            <span>Uses YOUR clothes</span>
          </div>
          <button className="cc-primary-btn" onClick={nextStep}>
            Let's Go
          </button>
        </div>
      )}

      {/* =========================
         STEP 1 – MOOD
         ========================= */}
      {step === 1 && (
        <div className="cc-step-card slide-in">
          <h3>What's Your Vibe Today?</h3>
          <p>Your mood shapes your style. How are you feeling?</p>

          <div className="cc-option-pills">
            {[
              { value: 'casual', label: 'Casual', desc: 'Laid-back & easy' },
              { value: 'confident', label: 'Confident', desc: 'Bold & powerful' },
              { value: 'relaxed', label: 'Relaxed', desc: 'Calm & comfortable' },
              { value: 'energetic', label: 'Energetic', desc: 'Active & vibrant' }
            ].map(option => (
              <button
                key={option.value}
                className={`cc-option-pill ${formData.mood === option.value ? 'active' : ''}`}
                onClick={() => handleChange('mood', option.value)}
              >
                <span className="cc-pill-label">{option.label}</span>
                <span className="cc-pill-desc">{option.desc}</span>
              </button>
            ))}
          </div>

          <div className="cc-step-buttons">
            <button className="cc-secondary-btn" onClick={prevStep}>
              ← Back
            </button>
            <button
              className="cc-primary-btn"
              disabled={!formData.mood}
              onClick={nextStep}
            >
              Next →
            </button>
          </div>
        </div>
      )}

      {/* =========================
         STEP 2 – OCCASION
         ========================= */}
      {step === 2 && (
        <div className="cc-step-card slide-in">
          <h3>Where Are You Headed?</h3>
          <p>Different places call for different styles. What's on your agenda?</p>

          <div className="cc-option-pills">
            {[
              { value: 'daily', label: 'Daily Wear', desc: 'Everyday comfort' },
              { value: 'college', label: 'College/Office', desc: 'Smart casual' },
              { value: 'party', label: 'Party', desc: 'Night out ready' },
              { value: 'formal', label: 'Formal Event', desc: 'Dress to impress' }
            ].map(option => (
              <button
                key={option.value}
                className={`cc-option-pill ${formData.occasion === option.value ? 'active' : ''}`}
                onClick={() => handleChange('occasion', option.value)}
              >
                <span className="cc-pill-label">{option.label}</span>
                <span className="cc-pill-desc">{option.desc}</span>
              </button>
            ))}
          </div>

          <div className="cc-step-buttons">
            <button className="cc-secondary-btn" onClick={prevStep}>
              ← Back
            </button>
            <button
              className="cc-primary-btn"
              disabled={!formData.occasion}
              onClick={nextStep}
            >
              Next →
            </button>
          </div>
        </div>
      )}

      {/* =========================
         STEP 3 – WEATHER
         ========================= */}
      {step === 3 && (
        <div className="cc-step-card slide-in">
          <h3>What's the Weather Like?</h3>
          <p>Let's make sure you're comfortable all day long.</p>

          <div className="cc-option-pills">
            {[
              { value: 'hot', label: 'Hot', desc: 'Light & breezy' },
              { value: 'moderate', label: 'Moderate', desc: 'Just right' },
              { value: 'cold', label: 'Cold', desc: 'Layer up' },
              { value: 'rainy', label: 'Rainy', desc: 'Stay dry' }
            ].map(option => (
              <button
                key={option.value}
                className={`cc-option-pill ${formData.weather === option.value ? 'active' : ''}`}
                onClick={() => handleChange('weather', option.value)}
              >
                <span className="cc-pill-label">{option.label}</span>
                <span className="cc-pill-desc">{option.desc}</span>
              </button>
            ))}
          </div>

          <div className="cc-step-buttons">
            <button className="cc-secondary-btn" onClick={prevStep}>
              ← Back
            </button>
            <button
              className={`cc-primary-btn cc-generate-btn ${isLoading ? 'loading' : ''}`}
              disabled={!formData.weather || isLoading}
              onClick={handleGenerate}
            >
              {isLoading ? (
                <>
                  <span className="cc-spinner"></span>
                  Creating your look...
                </>
              ) : (
                'Generate My Outfit'
              )}
            </button>
          </div>
        </div>
      )}

      {/* =========================
         RESULT MODAL
         ========================= */}
      <Modal
        isOpen={showResult}
        onClose={() => setShowResult(false)}
        title="Your Perfect Outfit"
      >
        <div className="cc-result-content">
          <div className="cc-result-summary">
            <div className="cc-result-item">
              <span className="cc-result-label">Mood</span>
              <span className="cc-result-value">{formData.mood}</span>
            </div>
            <div className="cc-result-item">
              <span className="cc-result-label">Occasion</span>
              <span className="cc-result-value">{formData.occasion}</span>
            </div>
            <div className="cc-result-item">
              <span className="cc-result-label">Weather</span>
              <span className="cc-result-value">{formData.weather}</span>
            </div>
          </div>

          {/* Display outfit images from user's wardrobe */}
          {result?.outfitImages && Object.keys(result.outfitImages).length > 0 ? (
            <div className="cc-result-outfit">
              <h4>Here's what we recommend from your wardrobe:</h4>
              <div className="cc-outfit-images-grid">
                {Object.entries(result.outfitImages).map(([category, imageUrl]) => (
                  imageUrl && (
                    <div key={category} className="cc-outfit-image-item">
                      <img
                        src={imageUrl}
                        alt={category}
                        className="cc-outfit-item-img"
                      />
                      <span className="cc-outfit-item-label">{category}</span>
                      <span className="cc-outfit-item-name">{result.outfit?.[category]}</span>
                    </div>
                  )
                ))}
              </div>
            </div>
          ) : (
            <div className="cc-result-outfit">
              <h4>No items found</h4>
              <div className="cc-outfit-placeholder">
                <div className="cc-placeholder-icon-box">
                  <div className="cc-icon-hanger"></div>
                </div>
                <p>
                  Your wardrobe doesn't have enough items yet.
                  Please upload more clothes to your wardrobe to get personalized outfit recommendations.
                </p>
              </div>
            </div>
          )}

          {/* Display reasoning */}
          {result?.reasoning && (
            <div className="cc-outfit-reasoning">
              <h4>💡 Stylist Notes:</h4>
              <ul>
                {result.reasoning.map((reason, idx) => (
                  <li key={idx}>{reason}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="cc-result-actions">
            <button className="cc-secondary-btn" onClick={resetGenerator} disabled={isSaving}>
              Generate Another
            </button>
            <button
              className={`cc-primary-btn ${isSaving ? 'loading' : ''} ${saveSuccess ? 'success' : ''}`}
              onClick={handleSaveLook}
              disabled={isSaving || saveSuccess}
            >
              {isSaving ? (
                <>
                  <span className="cc-spinner"></span>
                  Saving...
                </>
              ) : saveSuccess ? (
                '✓ Saved!'
              ) : (
                'Save This Look'
              )}
            </button>
          </div>
        </div>
      </Modal>
    </main>
  );
};

export default OutfitGenerator;
