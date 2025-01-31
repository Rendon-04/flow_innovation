import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';
import homepageImage from '../img/homepageImage.png'; 

const HomePage = () => {
  return (
    <div className="home-container">
      <div className="text-container">
        <h1 className="home-title">Welcome to Flow Innovation</h1>
        <p className="home-description">
          Flow Innovation is a platform designed to help you uncover truth and explore groundbreaking innovations.
          Use our Fact Check tool to verify claims and our Innovation News section to stay updated on the latest global advancements! 
        </p>
        <Link to="/innovation-news">
              <button className="homepage-button">News</button>
        </Link>
      </div>
      <div className="image-container">
        <img src={homepageImage} alt="Flow Innovation" className="homepage-image" />
      </div>
    </div>
  );
}

export default HomePage;

