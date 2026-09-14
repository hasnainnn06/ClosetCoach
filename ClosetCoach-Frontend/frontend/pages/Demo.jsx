import { useState, useEffect } from "react";
import Modal from "../src/components/Modal";
import { generateOutfitDemo, completeOutfitDemo, checkBackendHealth } from "../src/api";

const Demo = () => {
    // Tab state: 'generate' or 'complete'
    const [activeTab, setActiveTab] = useState("generate");

    /* =========================
       Scroll Animation
       ========================= */
    useEffect(() => {
        const items = document.querySelectorAll(".reveal");

        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("active");
                    }
                });
            },
            { threshold: 0.15 }
        );

        items.forEach(item => observer.observe(item));

        return () => items.forEach(item => observer.unobserve(item));
    }, []);

    // =========================================
    // Backend Health Check
    // =========================================
    const [backendOnline, setBackendOnline] = useState(null); // null=checking, true/false

    useEffect(() => {
        const checkHealth = async () => {
            const isHealthy = await checkBackendHealth();
            setBackendOnline(isHealthy);
        };
        checkHealth();
    }, []);

    // =========================================
    // Task 1: Generate Outfit State
    // =========================================
    const [generateStep, setGenerateStep] = useState(0);
    const [generateForm, setGenerateForm] = useState({
        gender: "",
        mood: "",
        occasion: "",
        weather: ""
    });
    const [isGenerating, setIsGenerating] = useState(false);
    const [showGenerateResult, setShowGenerateResult] = useState(false);
    const [generateResult, setGenerateResult] = useState(null);
    const [generateError, setGenerateError] = useState(null);

    // =========================================
    // Task 2: Complete Outfit State
    // =========================================
    const [completeStep, setCompleteStep] = useState(0);
    const [completeForm, setCompleteForm] = useState({
        image: null,
        imagePreview: null,
        gender: "",
        category: "",
        mood: "",
        occasion: "",
        weather: ""
    });
    const [isCompleting, setIsCompleting] = useState(false);
    const [showCompleteResult, setShowCompleteResult] = useState(false);
    const [completeResult, setCompleteResult] = useState(null);
    const [completeError, setCompleteError] = useState(null);

    // =========================================
    // Task 1 Handlers
    // =========================================
    const generateNextStep = () => setGenerateStep(prev => prev + 1);
    const generatePrevStep = () => setGenerateStep(prev => prev - 1);

    const handleGenerateChange = (key, value) => {
        setGenerateForm({ ...generateForm, [key]: value });
    };

    const handleGenerate = async () => {
        setIsGenerating(true);
        setGenerateError(null);

        try {
            const result = await generateOutfitDemo({
                gender: generateForm.gender,
                mood: generateForm.mood,
                occasion: generateForm.occasion,
                weather: generateForm.weather
            });

            if (result.success) {
                setGenerateResult(result);
                setShowGenerateResult(true);
                setBackendOnline(true);
            } else {
                setGenerateError(result.error || "Failed to generate outfit. Please try again.");
            }
        } catch (error) {
            // Re-check backend health to give a specific error message
            const isHealthy = await checkBackendHealth();
            setBackendOnline(isHealthy);
            if (!isHealthy) {
                setGenerateError("ML Backend is offline. Please start the backend server (python api.py) and try again.");
            } else {
                setGenerateError("Something went wrong while generating the outfit. Please try again.");
            }
        } finally {
            setIsGenerating(false);
        }
    };

    const resetGenerate = () => {
        setGenerateStep(0);
        setGenerateForm({ gender: "", mood: "", occasion: "", weather: "" });
        setShowGenerateResult(false);
        setGenerateResult(null);
        setGenerateError(null);
    };

    // =========================================
    // Task 2 Handlers
    // =========================================
    const completeNextStep = () => setCompleteStep(prev => prev + 1);
    const completePrevStep = () => setCompleteStep(prev => prev - 1);

    const handleCompleteChange = (key, value) => {
        setCompleteForm({ ...completeForm, [key]: value });
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
                setCompleteForm({
                    ...completeForm,
                    image: file,
                    imagePreview: reader.result
                });
            };
            reader.readAsDataURL(file);
        }
    };

    const handleComplete = async () => {
        setIsCompleting(true);
        setCompleteError(null);

        try {
            const result = await completeOutfitDemo({
                imageFile: completeForm.image,
                gender: completeForm.gender,
                category: completeForm.category,
                mood: completeForm.mood,
                occasion: completeForm.occasion,
                weather: completeForm.weather
            });

            if (result.success) {
                setCompleteResult(result);
                setShowCompleteResult(true);
                setBackendOnline(true);
            } else {
                setCompleteError(result.error || "Failed to find matching items. Please try again.");
            }
        } catch (error) {
            const isHealthy = await checkBackendHealth();
            setBackendOnline(isHealthy);
            if (!isHealthy) {
                setCompleteError("ML Backend is offline. Please start the backend server (python api.py) and try again.");
            } else {
                setCompleteError("Something went wrong while finding matches. Please try again.");
            }
        } finally {
            setIsCompleting(false);
        }
    };

    const resetComplete = () => {
        setCompleteStep(0);
        setCompleteForm({
            image: null,
            imagePreview: null,
            gender: "",
            category: "",
            mood: "",
            occasion: "",
            weather: ""
        });
        setShowCompleteResult(false);
        setCompleteResult(null);
        setCompleteError(null);
    };

    const generateTotalSteps = 4;
    const completeTotalSteps = 5;

    return (
        <main className="cc-demo-page">
            {/* Header Section */}
            <section className="cc-demo-header">
                <div className="cc-demo-badge fade-in-up">
                    <span className="cc-badge-icon">🧪</span>
                    <span>ML-Powered Dataset Demo</span>
                </div>
                <h1 className="fade-in-up delay-1">Experience AI Fashion Styling</h1>
                <p className="fade-in-up delay-2">
                    Try our pre-trained ML models powered by curated fashion datasets.
                    Generate complete outfits or find matching items — all without signing up!
                </p>
                <div className="cc-demo-disclaimer fade-in-up delay-3">
                    <span className="cc-disclaimer-icon">ℹ️</span>
                    <span>Results come from our training dataset — not your personal wardrobe</span>
                </div>
            </section>

            {/* Backend Status Banner */}
            {backendOnline === false && (
                <div className="cc-error-message" style={{ maxWidth: 600, margin: '0 auto 16px' }}>
                    <span>⚠️</span> ML Backend is offline. Please start the backend server ({<code>python api.py</code>}) to use the demo.
                </div>
            )}
            {backendOnline === true && (
                <div className="cc-demo-disclaimer fade-in-up" style={{ maxWidth: 600, margin: '0 auto 16px', background: '#ecfdf5', borderColor: '#86efac' }}>
                    <span className="cc-disclaimer-icon">✅</span>
                    <span>ML Backend is connected and ready</span>
                </div>
            )}

            {/* Tab Navigation */}
            <div className="cc-demo-tabs fade-in-up delay-4">
                <button
                    className={`cc-demo-tab ${activeTab === "generate" ? "active" : ""}`}
                    onClick={() => { setActiveTab("generate"); setGenerateStep(0); }}
                >
                    <span className="cc-tab-icon">✨</span>
                    <div className="cc-tab-content">
                        <span className="cc-tab-title">Generate Outfit</span>
                        <span className="cc-tab-desc">Get complete outfit suggestions</span>
                    </div>
                </button>
                <button
                    className={`cc-demo-tab ${activeTab === "complete" ? "active" : ""}`}
                    onClick={() => { setActiveTab("complete"); setCompleteStep(0); }}
                >
                    <span className="cc-tab-icon">🔍</span>
                    <div className="cc-tab-content">
                        <span className="cc-tab-title">Complete My Outfit</span>
                        <span className="cc-tab-desc">Find matching items for your piece</span>
                    </div>
                </button>
            </div>

            {/* =========================================
                TASK 1: GENERATE OUTFIT (Step-by-Step)
               ========================================= */}
            {activeTab === "generate" && (
                <div className="cc-demo-panel slide-in">
                    {/* Progress Bar */}
                    {generateStep > 0 && generateStep < generateTotalSteps && (
                        <div className="cc-progress-container">
                            <div className="cc-progress-bar">
                                <div
                                    className="cc-progress-fill"
                                    style={{ width: `${(generateStep / (generateTotalSteps - 1)) * 100}%` }}
                                ></div>
                            </div>
                            <span className="cc-progress-text">Step {generateStep} of {generateTotalSteps - 1}</span>
                        </div>
                    )}

                    {/* Error Message */}
                    {generateError && (
                        <div className="cc-error-message">
                            <span>⚠️</span> {generateError}
                        </div>
                    )}

                    {/* STEP 0 - Start */}
                    {generateStep === 0 && (
                        <div className="cc-step-card slide-in">
                            <div className="cc-step-icon-box">
                                <div className="cc-icon-sparkle"></div>
                            </div>
                            <h3>Generate a Complete Outfit</h3>
                            <p>
                                Answer 3 quick questions and let our ML model create
                                the perfect outfit from our fashion dataset!
                            </p>
                            <div className="cc-step-features">
                                <span>Takes 30 seconds</span>
                                <span>50,000+ items</span>
                                <span>AI-powered matching</span>
                            </div>
                            <button className="cc-primary-btn" onClick={generateNextStep}>
                                Let's Go
                            </button>
                        </div>
                    )}

                    {/* STEP 1 - Gender */}
                    {generateStep === 1 && (
                        <div className="cc-step-card slide-in">
                            <h3>What's Your Gender?</h3>
                            <p>Help us narrow down the perfect styles for you.</p>

                            <div className="cc-option-pills">
                                {[
                                    { value: 'female', label: 'Women', desc: 'Women\'s fashion' },
                                    { value: 'male', label: 'Men', desc: 'Men\'s fashion' }
                                ].map(option => (
                                    <button
                                        key={option.value}
                                        className={`cc-option-pill ${generateForm.gender === option.value ? 'active' : ''}`}
                                        onClick={() => handleGenerateChange('gender', option.value)}
                                    >
                                        <span className="cc-pill-label">{option.label}</span>
                                        <span className="cc-pill-desc">{option.desc}</span>
                                    </button>
                                ))}
                            </div>

                            <div className="cc-step-buttons">
                                <button className="cc-secondary-btn" onClick={generatePrevStep}>
                                    ← Back
                                </button>
                                <button
                                    className="cc-primary-btn"
                                    disabled={!generateForm.gender}
                                    onClick={generateNextStep}
                                >
                                    Next →
                                </button>
                            </div>
                        </div>
                    )}

                    {/* STEP 2 - Mood & Occasion */}
                    {generateStep === 2 && (
                        <div className="cc-step-card slide-in">
                            <h3>What's Your Vibe & Destination?</h3>
                            <p>Your mood and occasion shape your perfect outfit.</p>

                            <div className="cc-step-section">
                                <label className="cc-step-section-label">Your Vibe</label>
                                <div className="cc-option-pills">
                                    {[
                                        { value: 'casual', label: 'Casual', desc: 'Laid-back & easy' },
                                        { value: 'confident', label: 'Confident', desc: 'Bold & powerful' },
                                        { value: 'relaxed', label: 'Relaxed', desc: 'Calm & comfortable' },
                                        { value: 'energetic', label: 'Energetic', desc: 'Active & vibrant' }
                                    ].map(option => (
                                        <button
                                            key={option.value}
                                            className={`cc-option-pill ${generateForm.mood === option.value ? 'active' : ''}`}
                                            onClick={() => handleGenerateChange('mood', option.value)}
                                        >
                                            <span className="cc-pill-label">{option.label}</span>
                                            <span className="cc-pill-desc">{option.desc}</span>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="cc-step-section">
                                <label className="cc-step-section-label">Where Are You Headed?</label>
                                <div className="cc-option-pills">
                                    {[
                                        { value: 'daily', label: 'Daily Wear', desc: 'Everyday comfort' },
                                        { value: 'college', label: 'College/Office', desc: 'Smart casual' },
                                        { value: 'party', label: 'Party', desc: 'Night out ready' },
                                        { value: 'formal', label: 'Formal Event', desc: 'Dress to impress' }
                                    ].map(option => (
                                        <button
                                            key={option.value}
                                            className={`cc-option-pill ${generateForm.occasion === option.value ? 'active' : ''}`}
                                            onClick={() => handleGenerateChange('occasion', option.value)}
                                        >
                                            <span className="cc-pill-label">{option.label}</span>
                                            <span className="cc-pill-desc">{option.desc}</span>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="cc-step-buttons">
                                <button className="cc-secondary-btn" onClick={generatePrevStep}>
                                    ← Back
                                </button>
                                <button
                                    className="cc-primary-btn"
                                    disabled={!generateForm.mood || !generateForm.occasion}
                                    onClick={generateNextStep}
                                >
                                    Next →
                                </button>
                            </div>
                        </div>
                    )}

                    {/* STEP 3 - Weather */}
                    {generateStep === 3 && (
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
                                        className={`cc-option-pill ${generateForm.weather === option.value ? 'active' : ''}`}
                                        onClick={() => handleGenerateChange('weather', option.value)}
                                    >
                                        <span className="cc-pill-label">{option.label}</span>
                                        <span className="cc-pill-desc">{option.desc}</span>
                                    </button>
                                ))}
                            </div>

                            <div className="cc-step-buttons">
                                <button className="cc-secondary-btn" onClick={generatePrevStep}>
                                    ← Back
                                </button>
                                <button
                                    className={`cc-primary-btn cc-generate-btn ${isGenerating ? 'loading' : ''}`}
                                    disabled={!generateForm.weather || isGenerating}
                                    onClick={handleGenerate}
                                >
                                    {isGenerating ? (
                                        <>
                                            <span className="cc-spinner"></span>
                                            Querying ML Model...
                                        </>
                                    ) : (
                                        'Generate Outfit'
                                    )}
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* =========================================
                TASK 2: COMPLETE OUTFIT (Step-by-Step)
               ========================================= */}
            {activeTab === "complete" && (
                <div className="cc-demo-panel slide-in">
                    {/* Progress Bar */}
                    {completeStep > 0 && completeStep < completeTotalSteps && (
                        <div className="cc-progress-container">
                            <div className="cc-progress-bar">
                                <div
                                    className="cc-progress-fill"
                                    style={{ width: `${(completeStep / (completeTotalSteps - 1)) * 100}%` }}
                                ></div>
                            </div>
                            <span className="cc-progress-text">Step {completeStep} of {completeTotalSteps - 1}</span>
                        </div>
                    )}

                    {/* Error Message */}
                    {completeError && (
                        <div className="cc-error-message">
                            <span>⚠️</span> {completeError}
                        </div>
                    )}

                    {/* STEP 0 - Start */}
                    {completeStep === 0 && (
                        <div className="cc-step-card slide-in">
                            <div className="cc-step-icon-box">
                                <div className="cc-icon-camera"></div>
                            </div>
                            <h3>Complete Your Outfit</h3>
                            <p>
                                Got a piece you love? Upload it and our CIR model will find
                                the perfect matching items from our fashion dataset!
                            </p>
                            <div className="cc-step-features">
                                <span>4 quick steps</span>
                                <span>AI-powered matching</span>
                                <span>50,000+ items</span>
                            </div>
                            <button className="cc-primary-btn" onClick={completeNextStep}>
                                Let's Start
                            </button>
                        </div>
                    )}

                    {/* STEP 1 - Upload Image + Category */}
                    {completeStep === 1 && (
                        <div className="cc-step-card slide-in">
                            <h3>Upload Your Clothing Item</h3>
                            <p>Choose a piece you want to style around.</p>

                            <label className={`cc-cir-upload-box ${completeForm.imagePreview ? 'has-image' : ''}`}>
                                {completeForm.imagePreview ? (
                                    <div className="cc-cir-preview-container">
                                        <img src={completeForm.imagePreview} alt="Preview" className="cc-cir-preview-img" />
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

                            <div className="cc-step-section">
                                <label className="cc-step-section-label">What type of clothing is this?</label>
                                <div className="cc-option-pills cc-option-pills-row">
                                    {[
                                        { value: 'top', label: 'Top', desc: 'Shirt, T-shirt, Blouse' },
                                        { value: 'pants', label: 'Bottom', desc: 'Pants, Jeans, Skirt' }
                                    ].map(option => (
                                        <button
                                            key={option.value}
                                            className={`cc-option-pill ${completeForm.category === option.value ? 'active' : ''}`}
                                            onClick={() => handleCompleteChange('category', option.value)}
                                        >
                                            <span className="cc-pill-label">{option.label}</span>
                                            <span className="cc-pill-desc">{option.desc}</span>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="cc-step-section">
                                <label className="cc-step-section-label">Gender</label>
                                <div className="cc-option-pills cc-option-pills-row">
                                    {[
                                        { value: 'female', label: 'Women', desc: 'Women\'s fashion' },
                                        { value: 'male', label: 'Men', desc: 'Men\'s fashion' }
                                    ].map(option => (
                                        <button
                                            key={option.value}
                                            className={`cc-option-pill ${completeForm.gender === option.value ? 'active' : ''}`}
                                            onClick={() => handleCompleteChange('gender', option.value)}
                                        >
                                            <span className="cc-pill-label">{option.label}</span>
                                            <span className="cc-pill-desc">{option.desc}</span>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="cc-step-buttons">
                                <button className="cc-secondary-btn" onClick={completePrevStep}>
                                    ← Back
                                </button>
                                <button
                                    className="cc-primary-btn"
                                    disabled={!completeForm.imagePreview || !completeForm.category || !completeForm.gender}
                                    onClick={completeNextStep}
                                >
                                    Next →
                                </button>
                            </div>
                        </div>
                    )}

                    {/* STEP 2 - Mood */}
                    {completeStep === 2 && (
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
                                        className={`cc-option-pill ${completeForm.mood === option.value ? 'active' : ''}`}
                                        onClick={() => handleCompleteChange('mood', option.value)}
                                    >
                                        <span className="cc-pill-label">{option.label}</span>
                                        <span className="cc-pill-desc">{option.desc}</span>
                                    </button>
                                ))}
                            </div>

                            <div className="cc-step-buttons">
                                <button className="cc-secondary-btn" onClick={completePrevStep}>
                                    ← Back
                                </button>
                                <button
                                    className="cc-primary-btn"
                                    disabled={!completeForm.mood}
                                    onClick={completeNextStep}
                                >
                                    Next →
                                </button>
                            </div>
                        </div>
                    )}

                    {/* STEP 3 - Occasion */}
                    {completeStep === 3 && (
                        <div className="cc-step-card slide-in">
                            <h3>Where Are You Headed?</h3>
                            <p>Different places call for different styles.</p>

                            <div className="cc-option-pills">
                                {[
                                    { value: 'daily', label: 'Daily Wear', desc: 'Everyday comfort' },
                                    { value: 'office', label: 'Office/Work', desc: 'Smart casual' },
                                    { value: 'party', label: 'Party', desc: 'Night out ready' },
                                    { value: 'formal', label: 'Formal Event', desc: 'Dress to impress' }
                                ].map(option => (
                                    <button
                                        key={option.value}
                                        className={`cc-option-pill ${completeForm.occasion === option.value ? 'active' : ''}`}
                                        onClick={() => handleCompleteChange('occasion', option.value)}
                                    >
                                        <span className="cc-pill-label">{option.label}</span>
                                        <span className="cc-pill-desc">{option.desc}</span>
                                    </button>
                                ))}
                            </div>

                            <div className="cc-step-buttons">
                                <button className="cc-secondary-btn" onClick={completePrevStep}>
                                    ← Back
                                </button>
                                <button
                                    className="cc-primary-btn"
                                    disabled={!completeForm.occasion}
                                    onClick={completeNextStep}
                                >
                                    Next →
                                </button>
                            </div>
                        </div>
                    )}

                    {/* STEP 4 - Weather */}
                    {completeStep === 4 && (
                        <div className="cc-step-card slide-in">
                            <h3>What's the Weather Like?</h3>
                            <p>Let's make sure your outfit is weather-appropriate.</p>

                            <div className="cc-option-pills">
                                {[
                                    { value: 'hot', label: 'Hot', desc: 'Light & breezy' },
                                    { value: 'warm', label: 'Warm', desc: 'Just right' },
                                    { value: 'cool', label: 'Cool', desc: 'Slightly chilly' },
                                    { value: 'cold', label: 'Cold', desc: 'Layer up' }
                                ].map(option => (
                                    <button
                                        key={option.value}
                                        className={`cc-option-pill ${completeForm.weather === option.value ? 'active' : ''}`}
                                        onClick={() => handleCompleteChange('weather', option.value)}
                                    >
                                        <span className="cc-pill-label">{option.label}</span>
                                        <span className="cc-pill-desc">{option.desc}</span>
                                    </button>
                                ))}
                            </div>

                            <div className="cc-step-buttons">
                                <button className="cc-secondary-btn" onClick={completePrevStep}>
                                    ← Back
                                </button>
                                <button
                                    className={`cc-primary-btn cc-generate-btn ${isCompleting ? 'loading' : ''}`}
                                    disabled={!completeForm.weather || isCompleting}
                                    onClick={handleComplete}
                                >
                                    {isCompleting ? (
                                        <>
                                            <span className="cc-spinner"></span>
                                            Finding Matches...
                                        </>
                                    ) : (
                                        'Find Matching Items'
                                    )}
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* How It Works Section */}
            <section className="cc-demo-how-it-works reveal">
                <h2>How Our Demo Works</h2>
                <div className="cc-how-grid">
                    <div className="cc-how-card reveal">
                        <div className="cc-how-number">1</div>
                        <h4>Sample Dataset</h4>
                        <p>We use a curated dataset of 50,000+ fashion items with pre-computed style embeddings</p>
                    </div>
                    <div className="cc-how-card reveal">
                        <div className="cc-how-number">2</div>
                        <h4>ML Processing</h4>
                        <p>Your preferences are processed by our trained neural networks to understand style context</p>
                    </div>
                    <div className="cc-how-card reveal">
                        <div className="cc-how-number">3</div>
                        <h4>Smart Matching</h4>
                        <p>AI finds the best outfit combinations based on fashion compatibility principles</p>
                    </div>
                </div>
                <div className="cc-upgrade-note reveal">
                    <span>💡</span>
                    <span><strong>Want personalized results?</strong> Sign up to upload your wardrobe and get suggestions from your own clothes!</span>
                </div>
            </section>

            {/* Generate Result Modal */}
            <Modal
                isOpen={showGenerateResult}
                onClose={() => setShowGenerateResult(false)}
                title="Generated Outfit from Dataset"
            >
                <div className="cc-demo-result">
                    <div className="cc-demo-result-badge">
                        <span>🧪</span> ML Model Result
                    </div>

                    <div className="cc-demo-result-summary">
                        <div className="cc-result-item">
                            <span className="cc-result-label">Mood</span>
                            <span className="cc-result-value">{generateForm.mood}</span>
                        </div>
                        <div className="cc-result-item">
                            <span className="cc-result-label">Occasion</span>
                            <span className="cc-result-value">{generateForm.occasion}</span>
                        </div>
                        <div className="cc-result-item">
                            <span className="cc-result-label">Weather</span>
                            <span className="cc-result-value">{generateForm.weather}</span>
                        </div>
                    </div>

                    {generateResult?.outfitImage && (
                        <div className="cc-demo-outfit-image">
                            <h4>✨ Your AI-Generated Outfit:</h4>
                            <img
                                src={`data:image/png;base64,${generateResult.outfitImage}`}
                                alt="Generated Outfit"
                                className="cc-generated-outfit-img"
                            />
                        </div>
                    )}

                    {generateResult?.outfit && (
                        <div className="cc-demo-outfit-result">
                            <h4>🧠 Outfit Components:</h4>
                            <div className="cc-demo-outfit-items">
                                {Object.entries(generateResult.outfit).map(([key, value]) => (
                                    <div key={key} className="cc-demo-outfit-item">
                                        <span className="cc-outfit-category">{key}</span>
                                        <span className="cc-outfit-name">{Array.isArray(value) ? value.join(", ") : value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {generateResult?.reasoning && (
                        <div className="cc-demo-reasoning">
                            <h4>💡 Stylist Reasoning:</h4>
                            <ul>
                                {generateResult.reasoning.map((reason, idx) => (
                                    <li key={idx}>{reason}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    <div className="cc-demo-result-note">
                        <span>💡</span>
                        <span>This suggestion was generated from our training dataset. <strong>Sign up</strong> to get personalized suggestions from your own wardrobe!</span>
                    </div>

                    <div className="cc-result-actions">
                        <button className="cc-secondary-btn" onClick={resetGenerate}>
                            Try Again
                        </button>
                        <button className="cc-primary-btn" onClick={() => setShowGenerateResult(false)}>
                            Got It!
                        </button>
                    </div>
                </div>
            </Modal>

            {/* Complete Result Modal */}
            <Modal
                isOpen={showCompleteResult}
                onClose={() => setShowCompleteResult(false)}
                title="Matching Items from Dataset"
            >
                <div className="cc-demo-result">
                    <div className="cc-demo-result-badge">
                        <span>🎯</span> CIR Model Results
                    </div>

                    {completeForm.imagePreview && (
                        <div className="cc-demo-query-image">
                            <span>Your Uploaded Item:</span>
                            <img src={completeForm.imagePreview} alt="Query" />
                        </div>
                    )}

                    {completeResult?.matches && completeResult.matches.length > 0 ? (
                        <div className="cc-demo-matches">
                            <h4>🔍 Best Matches Found:</h4>
                            {completeResult.matches.map((match, index) => (
                                <div key={index} className="cc-demo-match-item">
                                    {match.imageBase64 && (
                                        <img
                                            src={`data:image/jpeg;base64,${match.imageBase64}`}
                                            alt={match.category}
                                            className="cc-match-image"
                                        />
                                    )}
                                    <div className="cc-match-info">
                                        <span className="cc-match-name">{match.category}</span>
                                        <span className="cc-match-category">Score: {match.score}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="cc-demo-no-matches">
                            <p>No matching items found. Try uploading a different image.</p>
                        </div>
                    )}

                    {completeResult?.reasoning && (
                        <div className="cc-demo-reasoning">
                            <h4>💡 Why these matches:</h4>
                            <ul>
                                {completeResult.reasoning.map((reason, idx) => (
                                    <li key={idx}>{reason}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    <div className="cc-demo-result-note">
                        <span>💡</span>
                        <span>These matches are from our training dataset. <strong>Upload your wardrobe</strong> to find matches from your own clothes!</span>
                    </div>

                    <div className="cc-result-actions">
                        <button className="cc-secondary-btn" onClick={resetComplete}>
                            Try Again
                        </button>
                        <button className="cc-primary-btn" onClick={() => setShowCompleteResult(false)}>
                            Got It!
                        </button>
                    </div>
                </div>
            </Modal>
        </main>
    );
};

export default Demo;
