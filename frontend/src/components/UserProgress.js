import React, { useState, useEffect } from 'react';
import './UserProgress.css';

const UserProgress = () => {
  const [progress, setProgress] = useState([]);
  const [achievement, setAchievement] = useState('');
  const [message, setMessage] = useState('');

  const fetchProgress = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await fetch("http://localhost:5001/progress", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
        }
      });
      const data = await response.json();
      if (response.ok) {
        setProgress(data.progress);  
      } else {
        setMessage(data.error || "⚠️ Failed to load progress.");
      }
    } catch (error) {
      console.error("❌ Fetch Error:", error);
      setMessage("⚠️ An error occurred while fetching progress.");
    }
  };

  useEffect(() => {
    fetchProgress(); 
  }, []);

  const handleAddProgress = async (e) => {
    e.preventDefault();
    setMessage("");

    if (!achievement.trim()) {
      setMessage("⚠️ Achievement cannot be empty.");
      return;
    }

    const requestBody = { achievement: achievement.trim() };

    try {
      const response = await fetch("http://localhost:5001/progress", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify(requestBody)
      });

      const data = await response.json();
      console.log("📥 Server response:", data);

      if (response.ok) {
        setMessage("✅ Progress added!");
        setAchievement('');
        fetchProgress();  
      } else {
        setMessage(data.error || "⚠️ Failed to add progress.");
      }
    } catch (error) {
      console.error("❌ Fetch Error:", error);
      setMessage("⚠️ An unexpected error occurred.");
    }
  };

  return (
    <div className="progress-container">
      <h2 className="progress-title">User Progress</h2>
      <form className="progress-form" onSubmit={handleAddProgress}>
        <input
          type="text"
          className="progress-input"
          value={achievement}
          onChange={(e) => setAchievement(e.target.value)}
          placeholder="Enter a new achievement"
          required
        />
        <button type="submit" className="progress-button">Add Progress</button>
      </form>
      {message && <p className="progress-message">{message}</p>}

      <h3 className="progress-list-title">Your Achievements:</h3>
      <ul className="progress-list">
        {progress.map((p) => (
          <li key={p.id} className="progress-item">
            <strong>{p.achievement}</strong> - {new Date(p.created_at).toLocaleDateString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserProgress;
