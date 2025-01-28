import React, { useState } from 'react';
import SearchBar from './SearchBar';
import ResultsBox from './ResultsBox';
import './FactCheckPage.css';

const FactCheckPage = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = (searchQuery) => {
    setQuery(searchQuery);
    setLoading(true);
    setError(null);

    fetch(`/check_claim?query=${encodeURIComponent(searchQuery)}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          setError(data.error);
          setResult(null);
        } else {
          setResult(data);
        }
        setLoading(false);
      })
      .catch(err => {
        setError('Error fetching fact check results');
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
      {result && <ResultsBox result={result} />}
    </div>
  );
};

export default FactCheckPage;
