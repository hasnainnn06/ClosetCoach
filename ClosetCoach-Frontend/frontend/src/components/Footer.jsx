import { Link } from "react-router-dom";

const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="cc-footer">
            <div className="cc-footer-container">
                {/* Brand Section */}
                <div className="cc-footer-brand">
                    <Link to="/" className="cc-footer-logo-link">
                        <div className="cc-footer-logo">CC</div>
                        <span className="cc-footer-brand-name">ClosetCoach</span>
                    </Link>
                    <p className="cc-footer-tagline">
                        Your AI-powered personal stylist. Transform your wardrobe, elevate your style.
                    </p>
                </div>

                {/* Quick Links */}
                <div className="cc-footer-links">
                    <h4>Explore</h4>
                    <Link to="/">Home</Link>
                    <Link to="/about">About</Link>
                    <Link to="/outfit-generator">Outfit Generator</Link>
                    <Link to="/cir">Complete Outfit</Link>
                </div>

                {/* Features */}
                <div className="cc-footer-links">
                    <h4>Features</h4>
                    <span>AI Style Analysis</span>
                    <span>Smart Recommendations</span>
                    <span>Wardrobe Management</span>
                    <span>Outfit History</span>
                </div>

                {/* Connect */}
                <div className="cc-footer-links">
                    <h4>Connect</h4>
                    <a href="mailto:hello@closetcoach.ai">Contact Us</a>
                    <span>Privacy Policy</span>
                    <span>Terms of Service</span>
                </div>
            </div>

            {/* Bottom Bar */}
            <div className="cc-footer-bottom">
                <p>© {currentYear} ClosetCoach. All rights reserved.</p>
                <p className="cc-footer-made">Made with ❤️ for fashion lovers everywhere</p>
            </div>
        </footer>
    );
};

export default Footer;
