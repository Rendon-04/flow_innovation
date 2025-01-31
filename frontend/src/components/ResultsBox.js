import React from 'react';
import './ResultsBox.css';

const ResultsBox = ({ result }) => {
  if (!result) return null; 

  return (
    <div className="results-box">
      <h3 className="results-title">Fact Check Result</h3>
      <p className="results-text">{result.text}</p>
      {result.claimReview && result.claimReview.length > 0 && (
        <a href={result.claimReview[0].url} target="_blank" rel="noopener noreferrer">
          Source: {result.claimReview[0].publisher.name}
        </a>
      )}
    </div>
  );
};

export default ResultsBox;
