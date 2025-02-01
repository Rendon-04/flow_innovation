import React, { useEffect, useState } from 'react';
import './UserProgress.css';

const UserProgress = () => {
  const [progress, setProgress] = useState([]);
  const [newAchievement, setNewAchievement] = useState('');

  useEffect(() => {
    fetch("http://localhost:5001/progress", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    })
    .then(response => response.json())
    .then(data => setProgress(data.progress || []))
    .catch(error => console.error("Error fetching progress:", error));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newAchievement) return;
  
    const response = await fetch("http://localhost:5001/progress", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ achievement: newAchievement })
    });
  
    if (response.ok) {
      const data = await response.json();
      setProgress([...progress, data]); 
      setNewAchievement(''); 
    } else {
      console.error("Error adding progress");
    }
  };

  return (
    <div className="progress-container">
      <h2 className="progress-title">User Progress</h2>
      <form onSubmit={handleSubmit} className="progress-form">
        <input
          type="text"
          value={newAchievement}
          onChange={(e) => setNewAchievement(e.target.value)}
          placeholder="Enter a new achievement"
          className="progress-input"
          required
        />
        <button type="submit" className="progress-button">Add Progress</button>
      </form>
      <ul className="progress-list">
        {progress.map((entry, index) => (
          <li key={index} className="progress-item">{entry.achievement}</li>
        ))}
      </ul>
    </div>
  );
};

export default UserProgress;

