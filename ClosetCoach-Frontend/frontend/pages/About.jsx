import { useEffect, useState } from "react";
import Modal from "../src/components/Modal";
import Footer from "../src/components/Footer";

const About = () => {
  const [selectedTech, setSelectedTech] = useState(null);

  // Scroll animation
  useEffect(() => {
    const items = document.querySelectorAll(".reveal");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("active");
          }
        });
      },
      { threshold: 0.15 },
    );
    items.forEach((item) => observer.observe(item));
    return () => items.forEach((item) => observer.unobserve(item));
  }, []);

  const techStack = [
    {
      id: "frontend",
      title: "Frontend",
      shortDesc:
        "React.js powers our responsive and interactive user interface.",
      fullDesc:
        "Built with React 19 and React Router for seamless navigation. The UI uses custom CSS with modern features like CSS variables, flexbox, and grid. Vite provides lightning-fast development and optimized builds.",
      features: [
        "React 19",
        "React Router 7",
        "Vite",
        "Custom CSS",
        "Responsive Design",
      ],
    },
    {
      id: "backend",
      title: "Backend",
      shortDesc: "Python Flask powers our REST API and ML pipeline.",
      fullDesc:
        "Flask serves our RESTful API with robust error handling. Firebase Admin SDK handles authentication and Firestore database access. TensorFlow powers the ML models for clothing classification and embedding extraction.",
      features: ["Python", "Flask", "REST API", "Firebase Auth", "TensorFlow"],
    },
    {
      id: "ml",
      title: "Machine Learning",
      shortDesc:
        "Trained models classify clothing and extract visual features.",
      fullDesc:
        "Our AI pipeline uses computer vision models for clothing classification, color extraction, and pattern recognition. The recommendation engine matches compatible items based on style rules and user preferences.",
      features: [
        "Image Classification",
        "Color Analysis",
        "Pattern Recognition",
        "Style Matching",
        "TensorFlow",
      ],
    },
    {
      id: "integration",
      title: "System Integration",
      shortDesc: "RESTful APIs enable seamless component interaction.",
      fullDesc:
        "Microservices architecture allows independent scaling of frontend, backend, and ML components. Real-time updates keep the wardrobe synced across devices.",
      features: [
        "Microservices",
        "API Gateway",
        "Real-time Sync",
        "Cloud Storage",
        "CDN",
      ],
    },
  ];

  return (
    <>
      <main className="cc-about">
        {/* =========================
           HERO / INTRO
           ========================= */}
        <section className="cc-about-hero reveal">
          <span className="cc-section-tag">Our Story</span>
          <h1>About ClosetCoach</h1>
          <p>
            We believe everyone deserves to look their best without spending
            hours deciding what to wear. ClosetCoach is your AI-powered personal
            stylist that works with what you already own.
          </p>
        </section>

        {/* =========================
           WHY SECTION
           ========================= */}
        <section className="cc-about-section cc-about-highlight reveal">
          <h2>Why We Built This</h2>
          <p>
            Every morning, millions of people stand in front of their closets
            feeling overwhelmed. "What should I wear?" becomes a daily struggle.
            We saw a problem that technology could solve — and we built
            ClosetCoach to make outfit decisions effortless, personalized, and
            even fun.
          </p>
        </section>

        {/* =========================
           MISSION
           ========================= */}
        <section className="cc-about-section reveal">
          <div className="cc-mission-grid">
            <div className="cc-mission-card">
              <div className="cc-mission-icon-box">
                <div className="cc-icon-target"></div>
              </div>
              <h3>Our Mission</h3>
              <p>
                To democratize personal styling by making AI-powered fashion
                advice accessible to everyone, using their own wardrobe.
              </p>
            </div>
            <div className="cc-mission-card">
              <div className="cc-mission-icon-box">
                <div className="cc-icon-eye"></div>
              </div>
              <h3>Our Vision</h3>
              <p>
                A world where looking great every day is effortless — where your
                closet works for you, not against you.
              </p>
            </div>
          </div>
        </section>

        {/* =========================
           TECHNOLOGY STACK
           ========================= */}
        <section className="cc-about-section reveal">
          <h2>Powered By Modern Tech</h2>
          <p className="cc-section-intro">
            Click on any card to learn more about the technology behind
            ClosetCoach.
          </p>

          <div className="cc-tech-grid">
            {techStack.map((tech) => (
              <div
                key={tech.id}
                className="cc-tech-card clickable"
                onClick={() => setSelectedTech(tech)}
              >
                <h4>{tech.title}</h4>
                <p>{tech.shortDesc}</p>
                <span className="cc-card-cta">Learn more →</span>
              </div>
            ))}
          </div>
        </section>

        {/* =========================
           TEAM SECTION
           ========================= */}
        <section className="cc-about-section cc-team-section reveal">
          <h2>Meet the Creators</h2>
          <div className="cc-team-grid">
            {/* Creator 1 */}
            <div className="cc-team-card">
              <div className="cc-team-avatar">
                <img src="/assets/images/hasnain.png" alt="Syed Hasnain Wasi" />
              </div>
              <div className="cc-team-info">
                <h3>Syed Hasnain Wasi</h3>
                <p className="cc-team-role">AI/ML & Data Science Enthusiast</p>
                <p className="cc-team-college">AMC Engineering College</p>
                <p className="cc-team-bio">
                  Passionate about building AI-powered solutions that make a
                  real difference. Specializing in machine learning and data
                  science to solve everyday problems.
                </p>
                <div className="cc-team-links">
                  <a
                    href="https://www.linkedin.com/in/syedhasnainwasi-/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="cc-team-link"
                  >
                    LinkedIn →
                  </a>
                </div>
              </div>
            </div>

            {/* Creator 2 */}
            <div className="cc-team-card">
              <div className="cc-team-avatar">
                <img src="/assets/images/shariq.jpg" alt="Shariq Ahmed" />
              </div>
              <div className="cc-team-info">
                <h3>Shariq Ahmed</h3>
                <p className="cc-team-role">Data Science Enthusiast</p>
                <p className="cc-team-college">AMC Engineering College</p>
                <p className="cc-team-bio">
                  Dedicated to exploring the intersection of data and
                  technology. Focused on creating impactful solutions through
                  data-driven insights.
                </p>
                <div className="cc-team-links">
                  <a
                    href="https://www.linkedin.com/in/shariq-ahmed-a37596243/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="cc-team-link"
                  >
                    LinkedIn →
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* =========================
           PROJECT GOALS
           ========================= */}
        <section className="cc-about-section reveal">
          <h2>Project Goals</h2>
          <div className="cc-goals-list">
            <div className="cc-goal-item">
              <span className="cc-goal-check"></span>
              <span>
                Demonstrate a user-centered fashion recommendation system
              </span>
            </div>
            <div className="cc-goal-item">
              <span className="cc-goal-check"></span>
              <span>Combine modern web technologies with machine learning</span>
            </div>
            <div className="cc-goal-item">
              <span className="cc-goal-check"></span>
              <span>Create an intuitive, beautiful user experience</span>
            </div>
            <div className="cc-goal-item">
              <span className="cc-goal-check"></span>
              <span>Build a scalable architecture for future enhancements</span>
            </div>
          </div>
        </section>
      </main>

      {/* Tech Detail Modal */}
      <Modal
        isOpen={!!selectedTech}
        onClose={() => setSelectedTech(null)}
        title={selectedTech?.title || ""}
      >
        {selectedTech && (
          <div className="cc-tech-modal-content">
            <h3>{selectedTech.title}</h3>
            <p className="cc-tech-modal-desc">{selectedTech.fullDesc}</p>
            <div className="cc-tech-features">
              <h4>Technologies Used:</h4>
              <div className="cc-feature-tags">
                {selectedTech.features.map((feature, idx) => (
                  <span key={idx} className="cc-feature-tag">
                    {feature}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </Modal>

      <Footer />
    </>
  );
};

export default About;
