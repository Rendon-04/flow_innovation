import React, { useState, useEffect, useCallback } from 'react';
import './GoalTracker.css';

const GoalTracker = () => {
  const [goal, setGoal] = useState('');
  const [targetDate, setTargetDate] = useState('');
  const [message, setMessage] = useState('');
  const [goals, setGoals] = useState([]);  
  const [aiRecommendations, setAiRecommendations] = useState([]);  

  const token = localStorage.getItem("token");

  // Fetch goals from backend
  const fetchGoals = useCallback(async () => {
    if (!token) return;

    try {
      const response = await fetch("http://localhost:5001/goals", {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
      });

      const data = await response.json();
      if (response.ok) {
        setGoals(data.goals);
      } else {
        setMessage(data.error || "⚠️ Failed to load goals.");
      }
    } catch (error) {
      console.error("❌ Fetch Error:", error);
      setMessage("⚠️ An error occurred while fetching goals.");
    }
  }, [token]);  

  useEffect(() => {
    fetchGoals();  
  }, [fetchGoals]);  

  // Handle goal submission
  const handleGoalSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    if (!goal.trim() || !targetDate) {
      setMessage("⚠️ Goal and target_date are required.");
      return;
    }

    const formattedDate = new Date(targetDate).toISOString().split("T")[0];

    const requestBody = {
      goal: goal.trim(),
      target_date: formattedDate
    };

    console.log("📤 Sending request:", requestBody);

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
        setGoal("");
        setTargetDate("");


        if (data.recommended_goals && data.recommended_goals.length > 0) {
          console.log("🧠 AI Recommended Goals:", data.recommended_goals);
          setAiRecommendations(data.recommended_goals);
        } else {
          setAiRecommendations([]);
        }

        fetchGoals(); 
      } else {
        setMessage(data.error || "⚠️ Failed to set goal.");
      }
    } catch (error) {
      console.error("❌ Fetch Error:", error);
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
        <input
          type="date"
          className="goal-date-input"
          value={targetDate}
          onChange={(e) => setTargetDate(e.target.value)}
          required
        />
        <button type="submit" className="goal-button">Set Goal</button>
      </form>
      {message && <p className="goal-message">{message}</p>}

      {/* Display Goals */}
      <h3 className="goal-list-title">Your Goals:</h3>
      <ul className="goal-list">
        {goals.map((g) => (
          <li key={g.id} className="goal-item">
            <strong>{g.goal}</strong> - {g.target_date}
          </li>
        ))}
      </ul>

      {/* 🔥 AI Recommendations */}
      {aiRecommendations.length > 0 && (
        <div className="ai-suggestions">
          <h3>🔍 AI-Suggested Goals:</h3>
          <ul className="goal-list">
            {aiRecommendations.map((rec, index) => (
              <li key={index} className="goal-item">{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default GoalTracker;
