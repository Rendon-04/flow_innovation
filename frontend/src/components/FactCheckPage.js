import React, { useState, useEffect } from 'react';
import SearchBar from './SearchBar';
import ResultsBox from './ResultsBox';
import './FactCheckPage.css';

const FactCheckPage = () => {
  console.log("FactCheckPage is rendering...");

  const [results, setResults] = useState([]); 
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    console.log("Updated results state:", results);
  }, [results]); 

  const handleSearch = (searchQuery) => {
    console.log("Search Triggered:", searchQuery);
    setLoading(true);
    setError(null);

    fetch(`http://localhost:5001/check_claim?query=${encodeURIComponent(searchQuery)}`)
      .then(response => response.json())
      .then(data => {
        console.log("Fact Check API Response:", data);
        if (data.claims && data.claims.length > 0) {
          setResults([...data.claims]);  
        } else {
          setResults([]);
          setError("No fact-checks found for this query.");
        }
        setLoading(false);
      })
      .catch(err => {
        setError("Error fetching fact check results");
        setLoading(false);
      });
  };

  return (
    <div className="fact-check-container">
      <h1 className="page-title-fact-check">Fact Checking</h1>
      <p className="description">Enter a claim to verify its authenticity using fact-checking sources.</p>
      <SearchBar onSearch={handleSearch} />
      {loading && <p className="loading">Checking...</p>}
      {error && <p className="error">{error}</p>}
      {results.length > 0 && (
        <div className="results-container">
          {results.map((result, index) => (
            <ResultsBox key={index} result={result} />
          ))}
        </div>
      )}
    </div>
  );
};

export default FactCheckPage;

