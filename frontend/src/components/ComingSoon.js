import React from 'react';
import './ComingSoon.css';

const ComingSoon = () => {
  return (
    <div className="coming-soon-container">
      <h1 className="coming-soon-title">Coming Soon</h1>
      <p className="coming-soon-description">Exciting features are on the way!</p>
      <ul className="coming-soon-list">
        <li className="coming-soon-item">User Profile Management - <span className="coming-soon-status">In Development</span></li>
        <li className="coming-soon-item">Achievements Leaderboard - <span className="coming-soon-status">Planned</span></li>
        <li className="coming-soon-item">Real-Time Notifications - <span className="coming-soon-status">In Planning</span></li>
      </ul>
    </div>
  );
};

export default ComingSoon;
