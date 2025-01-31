import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import logo from "../img/FlowInnovationNews.png"; 

const Navbar = () => {
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
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;


