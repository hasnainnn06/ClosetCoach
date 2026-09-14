import { useEffect } from "react";
import { Link } from "react-router-dom";
import Footer from "../src/components/Footer";

const Home = () => {
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

  return (
    <main className="cc-home">

      {/* =========================
          HERO SECTION
         ========================= */}
      <section className="cc-hero">
        <div className="cc-hero-inner">
          <div className="cc-hero-badge">
            <span className="cc-badge-dot"></span>
            AI-Powered Styling
          </div>

          <h1 className="cc-hero-title fade-in-up">
            Your Wardrobe,
            <br />
            <span className="cc-gradient-text">Intelligently Curated</span>
          </h1>

          <p className="cc-hero-subtitle fade-in-up delay-1">
            Stop staring at your closet wondering what to wear. ClosetCoach uses
            AI to transform your existing wardrobe into perfectly coordinated outfits
            — personalized for your style, mood, and the occasion.
          </p>

          <div className="cc-hero-tags fade-in-up delay-2">
            <span>AI Analysis</span>
            <span>Personal Wardrobe</span>
            <span>Smart Recommendations</span>
            <span>Privacy First</span>
          </div>

          <div className="cc-hero-cta fade-in-up delay-3">
            <Link to="/outfit-generator" className="cc-hero-btn cc-btn-primary">
              <span>Generate My Outfit</span>
              <span className="cc-btn-arrow">→</span>
            </Link>
            <Link to="/about" className="cc-hero-btn cc-btn-secondary">
              Learn More
            </Link>
          </div>

          <div className="cc-hero-stats fade-in-up delay-4">
            <div className="cc-stat">
              <span className="cc-stat-number">10K+</span>
              <span className="cc-stat-label">Outfits Generated</span>
            </div>
            <div className="cc-stat-divider"></div>
            <div className="cc-stat">
              <span className="cc-stat-number">98%</span>
              <span className="cc-stat-label">Style Match Rate</span>
            </div>
            <div className="cc-stat-divider"></div>
            <div className="cc-stat">
              <span className="cc-stat-number">5 min</span>
              <span className="cc-stat-label">Average Setup</span>
            </div>
          </div>
        </div>
      </section>

      {/* =========================
          FEATURES SECTION
         ========================= */}
      <section className="cc-features-section">
        <div className="cc-section-header reveal">
          <span className="cc-section-tag">Why ClosetCoach?</span>
          <h2 className="cc-section-title">Everything You Need to Look Your Best</h2>
          <p className="cc-section-subtitle">
            Whether you're a busy professional, a fashion-forward student, or anyone
            who wants to look great without the hassle — we've got you covered.
          </p>
        </div>

        <div className="cc-features-grid">
          <div className="cc-feature-card reveal">
            <div className="cc-feature-icon-box">
              <div className="cc-icon-upload"></div>
            </div>
            <h3>Upload Once, Style Forever</h3>
            <p>
              Simply photograph your clothes and let our AI catalog them.
              Your digital wardrobe syncs across all your devices.
            </p>
          </div>

          <div className="cc-feature-card reveal">
            <div className="cc-feature-icon-box">
              <div className="cc-icon-palette"></div>
            </div>
            <h3>Color & Style Matching</h3>
            <p>
              Our ML models analyze colors, patterns, and styles to create
              outfits that actually work together.
            </p>
          </div>

          <div className="cc-feature-card reveal">
            <div className="cc-feature-icon-box">
              <div className="cc-icon-weather"></div>
            </div>
            <h3>Weather-Smart Suggestions</h3>
            <p>
              Get outfit recommendations that match the day's weather —
              never overdress or underdress again.
            </p>
          </div>

          <div className="cc-feature-card reveal">
            <div className="cc-feature-icon-box">
              <div className="cc-icon-calendar"></div>
            </div>
            <h3>Occasion-Ready Looks</h3>
            <p>
              From boardroom meetings to weekend brunches, get outfits
              tailored to where you're going.
            </p>
          </div>

          <div className="cc-feature-card reveal">
            <div className="cc-feature-icon-box">
              <div className="cc-icon-bolt"></div>
            </div>
            <h3>Instant Recommendations</h3>
            <p>
              No more decision fatigue. Get personalized outfit suggestions
              in seconds, not minutes.
            </p>
          </div>

          <div className="cc-feature-card reveal">
            <div className="cc-feature-icon-box">
              <div className="cc-icon-lock"></div>
            </div>
            <h3>Private & Secure</h3>
            <p>
              Your wardrobe data stays yours. We never share your
              personal style information.
            </p>
          </div>
        </div>
      </section>

      {/* =========================
          HOW IT WORKS – TIMELINE
         ========================= */}
      <section className="cc-timeline-section">
        <div className="cc-section-header reveal">
          <span className="cc-section-tag">Simple Process</span>
          <h2 className="cc-timeline-title">How It Works</h2>
        </div>

        <div className="cc-timeline">
          {/* Step 01 */}
          <div className="cc-timeline-item left reveal">
            <div className="cc-content">
              <span className="cc-step">01</span>
              <h4>Upload Your Clothes</h4>
              <p>
                Snap photos of your clothing items — shirts, pants, dresses,
                accessories. Each piece gets stored securely in your digital closet.
              </p>
            </div>
          </div>

          {/* Step 02 */}
          <div className="cc-timeline-item right reveal">
            <div className="cc-content">
              <span className="cc-step">02</span>
              <h4>AI Analysis Kicks In</h4>
              <p>
                Our trained models classify each item by category, extract
                dominant colors, and understand textures and patterns.
              </p>
            </div>
          </div>

          {/* Step 03 */}
          <div className="cc-timeline-item left reveal">
            <div className="cc-content">
              <span className="cc-step">03</span>
              <h4>Get Personalized Outfits</h4>
              <p>
                Tell us your mood, occasion, and weather — we'll generate
                complete outfit combinations from YOUR wardrobe.
              </p>
            </div>
          </div>

          {/* Step 04 */}
          <div className="cc-timeline-item right reveal">
            <div className="cc-content">
              <span className="cc-step">04</span>
              <h4>Look Amazing Every Day</h4>
              <p>
                Save your favorite combinations, discover new pairings,
                and never second-guess your outfit again.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* =========================
          PERFECT FOR SECTION
         ========================= */}
      <section className="cc-audience-section">
        <div className="cc-section-header reveal">
          <span className="cc-section-tag">For Everyone</span>
          <h2 className="cc-section-title">Perfect For Your Lifestyle</h2>
        </div>

        <div className="cc-audience-grid">
          <div className="cc-audience-card reveal">
            <div className="cc-audience-icon">
              <div className="cc-icon-briefcase"></div>
            </div>
            <h4>Busy Professionals</h4>
            <p>
              Save precious morning time. Get work-appropriate outfits
              that command respect and exude confidence.
            </p>
          </div>

          <div className="cc-audience-card reveal">
            <div className="cc-audience-icon">
              <div className="cc-icon-book"></div>
            </div>
            <h4>Students</h4>
            <p>
              Look stylish on a budget. Maximize your wardrobe with
              creative combinations you never thought of.
            </p>
          </div>

          <div className="cc-audience-card reveal">
            <div className="cc-audience-icon">
              <div className="cc-icon-sparkle"></div>
            </div>
            <h4>Fashion Enthusiasts</h4>
            <p>
              Discover new outfit possibilities. Let AI inspire you
              with fresh takes on your existing collection.
            </p>
          </div>

          <div className="cc-audience-card reveal">
            <div className="cc-audience-icon">
              <div className="cc-icon-activity"></div>
            </div>
            <h4>Active Lifestyles</h4>
            <p>
              From gym to office to dinner. Plan your day's outfits
              for every activity seamlessly.
            </p>
          </div>
        </div>
      </section>

      {/* =========================
          CTA SECTION
         ========================= */}
      <section className="cc-cta-section reveal">
        <div className="cc-cta-content">
          <h2>Ready to Transform Your Style?</h2>
          <p>
            Join thousands who've already simplified their mornings
            and elevated their style game.
          </p>
          <Link to="/signup" className="cc-hero-btn cc-btn-primary cc-btn-large">
            <span>Get Started — It's Free</span>
            <span className="cc-btn-arrow">→</span>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </main>
  );
};

export default Home;
