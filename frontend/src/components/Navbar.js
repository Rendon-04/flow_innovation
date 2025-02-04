import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';
import logo from "../img/FlowInnovationNews.png";

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const navigate = useNavigate();

  useEffect(() => {
    const handleStorageChange = () => {
      setIsLoggedIn(!!localStorage.getItem('token'));
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <img src={logo} alt="Flow Innovation Logo" className="navbar-logo-img" />
        </Link>
        <ul className="navbar-links">
          <li className="navbar-item">
            <Link to="/">
              <button className="navbar-button">Home</button>
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/fact-check">
              <button className="navbar-button">Fact Check</button>
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/innovation-news">
              <button className="navbar-button">Innovation News</button>
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/progress-tracking">
              <button className="navbar-button">Progress Tracking</button>
            </Link>
          </li>
          {!isLoggedIn ? (
            <>
              <li className="navbar-item">
                <Link to="/register">
                  <button className="navbar-button">Register</button>
                </Link>
              </li>
              <li className="navbar-item">
                <Link to="/login">
                  <button className="navbar-button">Login</button>
                </Link>
              </li>
            </>
          ) : (
            <li className="navbar-item">
              <button className="navbar-button" onClick={handleLogout}>Logout</button>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
