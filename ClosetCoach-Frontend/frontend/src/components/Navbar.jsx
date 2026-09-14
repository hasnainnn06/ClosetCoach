import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const { user, logout } = useAuth();

  const isActive = (path) => location.pathname === path;

  const handleLogout = async () => {
    try {
      await logout();
      setMenuOpen(false);
      navigate("/");
    } catch (error) {
      console.error("Failed to logout:", error);
    }
  };

  // Get user's display name or email
  const getUserDisplayName = () => {
    if (user?.displayName) return user.displayName;
    if (user?.email) return user.email.split("@")[0];
    return "User";
  };

  return (
    <header className="cc-navbar">
      <div className="cc-nav-left">
        <Link to="/" className="cc-logo-link">
          <div className="cc-logo">CC</div>
          <span className="cc-brand">ClosetCoach</span>
        </Link>
      </div>

      {/* Mobile hamburger button */}
      <button
        className={`cc-hamburger ${menuOpen ? 'active' : ''}`}
        onClick={() => setMenuOpen(!menuOpen)}
        aria-label="Toggle menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <nav className={`cc-nav-center ${menuOpen ? 'open' : ''}`}>
        <Link to="/" className={isActive('/') ? 'active' : ''}>Home</Link>
        {user && (
          <>
            <Link to="/wardrobe" className={isActive('/wardrobe') ? 'active' : ''}>My Wardrobe</Link>
            <Link to="/outfit-generator" className={isActive('/outfit-generator') ? 'active' : ''}>Outfit Generator</Link>
            <Link to="/cir" className={isActive('/cir') ? 'active' : ''}>Complete Outfit</Link>
          </>
        )}
        <Link to="/demo" className={isActive('/demo') ? 'active' : ''}>Demo</Link>
        {user && (
          <Link to="/saved-looks" className={isActive('/saved-looks') ? 'active' : ''}>Saved Looks</Link>
        )}
        <Link to="/about" className={isActive('/about') ? 'active' : ''}>About</Link>
      </nav>

      <div className={`cc-nav-right ${menuOpen ? 'open' : ''}`}>
        {user ? (
          <>
            <span className="cc-user-greeting">Hi, {getUserDisplayName()}</span>
            <button onClick={handleLogout} className="cc-logout-btn">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="cc-login">Login</Link>
            <Link to="/signup" className="cc-signup">Get Started</Link>
          </>
        )}
      </div>
    </header>
  );
};

export default Navbar;
