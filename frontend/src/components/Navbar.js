import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">Flow Innovation</Link>
        <ul className="navbar-links">
          <li className="navbar-item">
            <Link to="/" className="navbar-link">Home</Link>
          </li>
          <li className="navbar-item">
            <Link to="/fact-check" className="navbar-link">Fact Check</Link>
          </li>
          <li className="navbar-item">
            <Link to="/innovation-news" className="navbar-link">Innovation News</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
