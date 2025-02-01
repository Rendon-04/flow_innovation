import React from 'react';
import UserProgress from './UserProgress';
import GoalTracker from './GoalTracker';
import CommunityProgress from './CommunityProgress';
import ProgressInsights from './ProgressInsights';
import './ProgressTracking.css';

const ProgressTracking = () => {
  return (
    <div className="progress-tracking-container">
      <h2 className="progress-tracking-title">Progress Tracking</h2>
      <div className="progress-sections">
        <div className="progress-section"><GoalTracker /></div>
        <div className="progress-section"><UserProgress /></div>
        <div className="progress-section"><CommunityProgress /></div>
        <div className="progress-section"><ProgressInsights /></div>
      </div>
    </div>
  );
};

export default ProgressTracking;

