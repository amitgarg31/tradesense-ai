import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

const Navbar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="navbar glass-card">
      <div className="container">
        <div className="navbar-content">
          <div className="navbar-brand">
            <span className="brand-icon">📈</span>
            <h2 className="brand-text">TradeSense AI</h2>
          </div>

          <div className="navbar-links">
            <Link
              to="/"
              className={`nav-link ${isActive("/") ? "active" : ""}`}
            >
              Dashboard
            </Link>
            <Link
              to="/analytics"
              className={`nav-link ${isActive("/analytics") ? "active" : ""}`}
            >
              Analytics
            </Link>
            <Link
              to="/insights"
              className={`nav-link ${isActive("/insights") ? "active" : ""}`}
            >
              AI Insights
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
