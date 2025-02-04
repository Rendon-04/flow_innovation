import React, { useEffect, useState } from 'react';
import './CommunityProgress.css';

const CommunityProgress = () => {
  const [progress, setProgress] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001//progress/community', {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`, 
      },
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => setProgress(data.progress)) 
      .catch(error => console.error('Error fetching community progress:', error));
  }, []);

  return (
    <div className="community-progress-container">
      <h2 className="community-title">Community Progress</h2>
      <ul className="community-list">
        {progress.length > 0 ? (
          progress.map((entry, index) => (
            <li key={index} className="community-item">{entry.achievement}</li>
          ))
        ) : (
          <p>No progress recorded yet.</p>
        )}
      </ul>
    </div>
  );
};

export default CommunityProgress;
