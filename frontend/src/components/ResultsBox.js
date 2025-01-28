import React from 'react';
import './ResultsBox.css';

const ResultsBox = ({ result }) => {
  return (
    <div className="results-box">
      <h2 className="results-title">Fact Check Results</h2>
      {result.claims && result.claims.length > 0 ? (
        result.claims.map((claim, index) => (
          <div key={index} className="result-item">
            <h3 className="claim-text">{claim.text}</h3>
            <p className="claim-review">{claim.claimReview ? claim.claimReview[0].textualRating : 'No rating available'}</p>
            {claim.claimReview && claim.claimReview[0].url && (
              <a href={claim.claimReview[0].url} target="_blank" rel="noopener noreferrer" className="fact-source">
                Source
              </a>
            )}
          </div>
        ))
      ) : (
        <p className="no-results">No fact check results found.</p>
      )}
    </div>
  );
};

export default ResultsBox;