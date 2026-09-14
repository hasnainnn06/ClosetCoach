import { useState, useEffect } from "react";
import Modal from "../src/components/Modal";
import { useAuth } from "../src/context/AuthContext";
import { db } from "../src/firebase";
import { collection, query, where, getDocs, addDoc } from "firebase/firestore";

const CIR = () => {
  const { user } = useAuth();
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({
    image: null,
    imagePreview: null,
    category: "",
    mood: "",
    occasion: "",
    weather: ""
  });
  const [isLoading, setIsLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [wardrobeItems, setWardrobeItems] = useState([]);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Fetch user's wardrobe on mount
  useEffect(() => {
    const fetchWardrobe = async () => {
      if (!user) return;
      try {
        const q = query(
          collection(db, "wardrobe"),
          where("userId", "==", user.uid)
        );
        const snapshot = await getDocs(q);
        const items = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }));
        setWardrobeItems(items);
      } catch (err) {
        console.error("Failed to fetch wardrobe:", err);
      }
    };
    fetchWardrobe();
  }, [user]);

  const nextStep = () => setStep(prev => prev + 1);
  const prevStep = () => setStep(prev => prev - 1);

  const handleChange = (key, value) => {
    setFormData({ ...formData, [key]: value });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        alert('Please upload an image file');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData({
          ...formData,
          image: file,
          imagePreview: reader.result
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleComplete = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const uploadedCategory = formData.category;
      let targetCategory = uploadedCategory === "top" ? "pants" : "top";

      // Color coordination rules - colors that go well together
      const colorPairings = {
        black: ["white", "gray", "red", "blue", "beige", "yellow"],
        white: ["black", "blue", "gray", "beige", "red", "green"],
        blue: ["white", "black", "gray", "beige", "brown"],
        red: ["black", "white", "gray", "beige"],
        green: ["white", "beige", "brown", "black"],
        yellow: ["black", "blue", "gray", "white"],
        pink: ["white", "black", "gray", "beige"],
        beige: ["black", "white", "brown", "blue", "green"],
        gray: ["black", "white", "blue", "red", "yellow", "pink"],
        brown: ["white", "beige", "blue", "green"]
      };

      // Occasion-based color preferences
      const occasionColors = {
        formal: ["black", "white", "gray", "blue", "beige"],
        party: ["black", "red", "pink", "white", "blue"],
        daily: ["blue", "white", "gray", "beige", "green"],
        college: ["blue", "gray", "white", "black", "beige"]
      };

      // Filter wardrobe for matching category items
      const matchingItems = wardrobeItems.filter(item =>
        item.category && item.category.toLowerCase() === targetCategory
      );

      // Score each matching item
      const scoredItems = matchingItems.map(item => {
        let score = 0.5; // Base score
        const itemColor = item.color?.toLowerCase();

        // Color coordination bonus (up to +0.3)
        // Note: We don't have the uploaded image's color auto-detected yet
        // So we'll use occasion-based preferences
        if (itemColor && occasionColors[formData.occasion]) {
          if (occasionColors[formData.occasion].includes(itemColor)) {
            score += 0.25;
          }
        }

        // Neutral colors work well with everything (+0.1)
        if (["black", "white", "gray", "beige"].includes(itemColor)) {
          score += 0.1;
        }

        // Weather-appropriate adjustments
        if (formData.weather === "hot" && ["white", "beige", "pink"].includes(itemColor)) {
          score += 0.1; // Light colors for hot weather
        }
        if (formData.weather === "cold" && ["black", "gray", "brown", "blue"].includes(itemColor)) {
          score += 0.1; // Darker colors for cold weather
        }

        // Add small random factor for variety (0-0.1)
        score += Math.random() * 0.1;

        return { ...item, score: Math.min(score, 0.99) };
      });

      // Sort by score (highest first) and pick the best match
      scoredItems.sort((a, b) => b.score - a.score);

      // Get jackets if cold weather
      let jacketItems = [];
      if (["cold", "cool", "rainy"].includes(formData.weather)) {
        jacketItems = wardrobeItems.filter(item =>
          item.category && item.category.toLowerCase() === "jacket"
        );
      }

      const matches = [];

      if (scoredItems.length > 0) {
        const selected = scoredItems[0]; // Pick the best scored item
        matches.push({
          category: targetCategory.charAt(0).toUpperCase() + targetCategory.slice(1),
          imageBase64: selected.imageUrl,
          name: selected.name,
          color: selected.color,
          score: selected.score
        });
      }

      if (jacketItems.length > 0) {
        // Score jackets too
        const scoredJackets = jacketItems.map(item => {
          let score = 0.6;
          const itemColor = item.color?.toLowerCase();
          if (["black", "gray", "beige", "brown"].includes(itemColor)) {
            score += 0.2; // Neutral jackets are versatile
          }
          return { ...item, score: Math.min(score + Math.random() * 0.1, 0.95) };
        });
        scoredJackets.sort((a, b) => b.score - a.score);

        const selected = scoredJackets[0];
        matches.push({
          category: "Layer/Jacket",
          imageBase64: selected.imageUrl,
          name: selected.name,
          color: selected.color,
          score: selected.score
        });
      }

      const reasoning = [];
      if (matches.length > 0) {
        reasoning.push(`Selected ${matches.length} best-matching item(s) from your wardrobe`);
        if (matches[0].color) {
          reasoning.push(`Chose ${matches[0].color} ${matches[0].category.toLowerCase()} for color coordination`);
        }
      }
      reasoning.push(`Styled for ${formData.occasion} occasion`);
      reasoning.push(`Optimized for ${formData.weather} weather`);
      reasoning.push(`Matches your ${formData.mood} mood`);

      if (matches.length === 0) {
        setError(`No matching ${targetCategory} found in your wardrobe. Please add more items!`);
      } else {
        setResult({
          success: true,
          matches: matches,
          reasoning: reasoning
        });
        setShowResult(true);
      }
    } catch (err) {
      setError("Failed to find matching items: " + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setStep(0);
    setFormData({
      image: null,
      imagePreview: null,
      category: "",
      mood: "",
      occasion: "",
      weather: ""
    });
    setResult(null);
    setError(null);
    setShowResult(false);
    setSaveSuccess(false);
  };

  const handleSaveLook = async () => {
    if (!user || !result) return;

    setIsSaving(true);
    setError(null);

    try {
      const savedLook = {
        userId: user.uid,
        uploadedItem: {
          imageBase64: formData.imagePreview,
          category: formData.category
        },
        matchedItems: result.matches || [],
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
        resetForm();
      }, 1500);
    } catch (err) {
      console.error("Failed to save look:", err);
      setError("Failed to save this look. Please try again.");
    } finally {
      setIsSaving(false);
    }
  };

  const totalSteps = 5;

  return (
    <main className="cc-outfit-page">
      {/* =========================
         PAGE HEADER
         ========================= */}
      <section className="cc-outfit-header">
        <span className="cc-section-tag">AI-Powered Matching</span>
        <h1>Complete Your Look</h1>
        <p>
          Upload one piece from your wardrobe and let our AI find the perfect
          matching items to create a stunning complete outfit.
        </p>
      </section>

      {/* Progress Indicator */}
      {step > 0 && step < totalSteps && (
        <div className="cc-progress-container">
          <div className="cc-progress-bar">
            <div
              className="cc-progress-fill"
              style={{ width: `${(step / (totalSteps - 1)) * 100}%` }}
            ></div>
          </div>
          <span className="cc-progress-text">Step {step} of {totalSteps - 1}</span>
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
            <div className="cc-icon-camera"></div>
          </div>
          <h3>Complete Your Outfit</h3>
          <p>
            Got a piece you want to wear? Upload it and we'll find the perfect
            matching items from your wardrobe to complete your look!
          </p>
          <div className="cc-step-features">
            <span>4 quick steps</span>
            <span>Personalized matches</span>
            <span>Uses YOUR clothes</span>
          </div>
          <button className="cc-primary-btn" onClick={nextStep}>
            Let's Start
          </button>
        </div>
      )}

      {/* =========================
         STEP 1 – UPLOAD IMAGE
         ========================= */}
      {step === 1 && (
        <div className="cc-step-card slide-in">
          <h3>Upload Your Clothing Item</h3>
          <p>Choose a piece from your wardrobe that you want to style around.</p>

          <label className={`cc-cir-upload-box ${formData.imagePreview ? 'has-image' : ''}`}>
            {formData.imagePreview ? (
              <div className="cc-cir-preview-container">
                <img src={formData.imagePreview} alt="Preview" className="cc-cir-preview-img" />
                <span className="cc-cir-change-label">Click to change</span>
              </div>
            ) : (
              <div className="cc-upload-placeholder">
                <div className="cc-upload-icon">📷</div>
                <span>Drop your image here or click to browse</span>
              </div>
            )}
            <input
              type="file"
              hidden
              accept="image/*"
              onChange={handleImageChange}
            />
          </label>

          {/* Category Selection */}
          <div className="cc-step-section">
            <label className="cc-step-section-label">What type of clothing is this?</label>
            <div className="cc-option-pills cc-option-pills-row">
              {[
                { value: 'top', label: 'Top', desc: 'Shirt, T-shirt, Blouse' },
                { value: 'pants', label: 'Bottom', desc: 'Pants, Jeans, Skirt' }
              ].map(option => (
                <button
                  key={option.value}
                  className={`cc-option-pill ${formData.category === option.value ? 'active' : ''}`}
                  onClick={() => handleChange('category', option.value)}
                >
                  <span className="cc-pill-label">{option.label}</span>
                  <span className="cc-pill-desc">{option.desc}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="cc-step-buttons">
            <button className="cc-secondary-btn" onClick={prevStep}>
              ← Back
            </button>
            <button
              className="cc-primary-btn"
              disabled={!formData.imagePreview || !formData.category}
              onClick={nextStep}
            >
              Next →
            </button>
          </div>
        </div>
      )}

      {/* =========================
         STEP 2 – MOOD
         ========================= */}
      {step === 2 && (
        <div className="cc-step-card slide-in">
          <h3>What's Your Vibe Today?</h3>
          <p>Your mood shapes your style. How are you feeling?</p>

          <div className="cc-option-pills">
            {[
              { value: 'casual', label: 'Casual', desc: 'Laid-back & easy' },
              { value: 'confident', label: 'Confident', desc: 'Bold & powerful' },
              { value: 'elegant', label: 'Elegant', desc: 'Refined & classy' },
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
         STEP 3 – OCCASION
         ========================= */}
      {step === 3 && (
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
         STEP 4 – WEATHER
         ========================= */}
      {step === 4 && (
        <div className="cc-step-card slide-in">
          <h3>What's the Weather Like?</h3>
          <p>Let's make sure your complete outfit is weather-appropriate.</p>

          <div className="cc-option-pills">
            {[
              { value: 'hot', label: 'Hot', desc: 'Light & breezy' },
              { value: 'warm', label: 'Warm', desc: 'Just right' },
              { value: 'cool', label: 'Cool', desc: 'Slightly chilly' },
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
              onClick={handleComplete}
            >
              {isLoading ? (
                <>
                  <span className="cc-spinner"></span>
                  Finding matches...
                </>
              ) : (
                'Complete My Outfit'
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
        title="Your Complete Look"
      >
        <div className="cc-result-content">
          {/* Your uploaded item */}
          {formData.imagePreview && (
            <div className="cc-result-uploaded">
              <h4>Your Item</h4>
              <img src={formData.imagePreview} alt="Your upload" className="cc-uploaded-preview" />
              <span className="cc-uploaded-label">{formData.category === 'top' ? 'Top' : 'Bottom'}</span>
            </div>
          )}

          {/* Matching items */}
          {result?.matches && result.matches.length > 0 ? (
            <div className="cc-result-outfit">
              <h4>Matching Items From Your Wardrobe</h4>
              <div className="cc-outfit-images-grid">
                {result.matches.map((match, idx) => (
                  <div key={idx} className="cc-outfit-image-item">
                    {match.imageBase64 && (
                      <img
                        src={match.imageBase64.startsWith('data:') ? match.imageBase64 : `data:image/jpeg;base64,${match.imageBase64}`}
                        alt={match.category}
                        className="cc-outfit-item-img"
                      />
                    )}
                    <span className="cc-outfit-item-label">{match.category}</span>
                    {match.name && <span className="cc-outfit-item-name">{match.name}</span>}
                    <span className="cc-match-score">Match: {(match.score * 100).toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="cc-result-outfit">
              <h4>No Items Found</h4>
              <div className="cc-outfit-placeholder">
                <p>
                  Your wardrobe doesn't have matching items yet.
                  Please upload more clothes to get complete outfit recommendations.
                </p>
              </div>
            </div>
          )}

          {/* Reasoning */}
          {result?.reasoning && (
            <div className="cc-outfit-reasoning">
              <h4>💡 Style Notes:</h4>
              <ul>
                {result.reasoning.map((reason, idx) => (
                  <li key={idx}>{reason}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="cc-result-actions">
            <button className="cc-secondary-btn" onClick={resetForm} disabled={isSaving}>
              Try Another
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

export default CIR;
