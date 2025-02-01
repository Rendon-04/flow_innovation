import React, { useEffect, useState } from 'react';
import './ProgressInsights.css';

const ProgressInsights = () => {
  const [insights, setInsights] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5001/wolfram/progress_insights', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 1 })
    })
      .then(response => response.json())
      .then(data => setInsights(data))
      .catch(error => console.error('Error fetching insights:', error));
  }, []);

  return (
    <div className="progress-insights-container">
      <h2 className="insights-title">Progress Insights</h2>
      {insights ? (
        <div className="insights-content">
          <p>Next Milestone: {insights.next_milestone}</p>
          <p>Innovation Score: {insights.innovation_score}</p>
          <p>Suggestions: {insights.suggestions}</p>
        </div>
      ) : (
        <p>Loading insights...</p>
      )}
    </div>
  );
};

export default ProgressInsights;
