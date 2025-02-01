import React, { useEffect, useState } from 'react';
import './CommunityProgress.css';

const CommunityProgress = () => {
  const [progress, setProgress] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/community-progress')
      .then(response => response.json())
      .then(data => setProgress(data.progress))
      .catch(error => console.error('Error fetching community progress:', error));
  }, []);

  return (
    <div className="community-progress-container">
      <h2 className="community-title">Community Progress</h2>
      <ul className="community-list">
        {progress.map((entry, index) => (
          <li key={index} className="community-item">{entry.progress_story}</li>
        ))}
      </ul>
    </div>
  );
};

export default CommunityProgress;