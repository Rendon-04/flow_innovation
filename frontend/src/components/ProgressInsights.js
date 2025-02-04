import React, { useEffect, useState } from "react";
import "./ProgressInsights.css";

const ProgressInsights = () => {
  const [insights, setInsights] = useState(null);
  const [error, setError] = useState(null);
  const API_BASE_URL = "http://127.0.0.1:5001";

  useEffect(() => {
    
    const token = localStorage.getItem("token");

    if (!token) {
      setError("Unauthorized: Missing JWT token.");
      return;
    }

    fetch(`${API_BASE_URL}/wolfram/progress_insights`, {
      method: "GET", 
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}` 
      }
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.error || "Unknown error"); });
      }
      return response.json();
    })
    .then(data => setInsights(data))
    .catch(error => {
      console.error("❌ Error fetching insights:", error);
      setError(error.message);
    });
  }, []);

  return (
    <div className="progress-insights-container">
      <h2 className="insights-title">Progress Insights</h2>
      {error ? (
        <p className="error-message">Error: {error}</p>
      ) : insights ? (
        <div className="insights-content">
          <p><strong>Next Milestone:</strong> {insights.next_milestone || "N/A"}</p>
          <p><strong>Innovation Score:</strong> {insights.innovation_score || "N/A"}</p>
          <p><strong>Suggestions:</strong> {insights.suggestions?.join(", ") || "No suggestions yet"}</p>
        </div>
      ) : (
        <p>Loading insights...</p>
      )}
    </div>
  );
};

export default ProgressInsights;
