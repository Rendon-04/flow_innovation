import React, { useState } from 'react';
import './GoalTracker.css';

const GoalTracker = () => {
  const [goal, setGoal] = useState('');
  const [message, setMessage] = useState('');

  const handleGoalSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
  
    const token = localStorage.getItem("token");
    if (!token) {
      setMessage("⚠️ You must be logged in to set a goal.");
      return;
    }
  
    if (!goal.trim()) {
      setMessage("⚠️ Please enter a goal.");
      return;
    }
  
    const requestBody = {
      goal: goal.trim(),  
    };
    console.log("📤 Final Request Body:", JSON.stringify(requestBody)); 
  
    try {
      const response = await fetch("http://localhost:5001/goal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(requestBody)
      });
  
      const data = await response.json();
      console.log("📥 Server response:", data);
  
      if (response.ok) {
        setMessage("✅ Goal successfully set!");
        setGoal('');
      } else {
        setMessage(data.error || "⚠️ Failed to set goal.");
      }
    } catch (error) {
      console.error("❌ Error:", error);
      setMessage("⚠️ An unexpected error occurred.");
    }
  };
  
  

  return (
    <div className="goal-container">
      <h2 className="goal-title">Goal Tracker</h2>
      <form className="goal-form" onSubmit={handleGoalSubmit}>
        <input
          type="text"
          className="goal-input"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="Enter your goal"
          required
        />
        <button type="submit" className="goal-button">Set Goal</button>
      </form>
      {message && <p className="goal-message">{message}</p>}
    </div>
  );
};

export default GoalTracker;
