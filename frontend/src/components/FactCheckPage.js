import React, { useState, useEffect } from "react";
import SearchBar from "./SearchBar";
import ResultsBox from "./ResultsBox";
import "./FactCheckPage.css";

const FactCheckPage = () => {
  console.log("FactCheckPage is rendering...");

  const [results, setResults] = useState([]); 
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    console.log("Updated results state:", results);
  }, [results]);

  const cleanPythonJSON = (rawData) => {
    try {
      if (typeof rawData !== "string") return rawData;
      console.log("🛠️ Raw cached_result before cleaning:", rawData);

      let fixedData = rawData
        .replace(/\bNone\b/g, "null")
        .replace(/\bTrue\b/g, "true")
        .replace(/\bFalse\b/g, "false");

      return JSON.parse(fixedData);
    } catch (error) {
      console.error("❌ JSON Parsing Failed:", error);
      return null;
    }
  };

  const handleSearch = async (searchQuery) => {
    console.log("🔍 Search Triggered:", searchQuery);
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:5001/check_claim?query=${encodeURIComponent(searchQuery)}`,
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }
      );

      if (!response.ok) {
        console.error("❌ API Error:", response.status);
        setError(`⚠️ API Error: ${response.status}`);
        setResults([]); 
        setLoading(false);
        return;
      }

      const jsonData = await response.json();
      console.log("✅ Parsed API Response:", jsonData);

      if (!jsonData || typeof jsonData !== "object") {
        console.error("❌ Invalid API Response:", jsonData);
        setError("⚠️ Invalid response from the server.");
        setResults([]);
        setLoading(false);
        return;
      }

      const claims = jsonData.cached_result?.claims || jsonData.claims;
      setResults(Array.isArray(claims) ? claims : []);
      if (!Array.isArray(claims) || claims.length === 0) {
        setError("⚠️ No fact-checks found for this query.");
      }
    } catch (error) {
      console.error("❌ Fetch Error:", error);
      setError("⚠️ Error fetching fact-check results.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fact-check-container">
      <h1 className="page-title-fact-check">Fact Checking</h1>
      <p className="description">
        Enter a claim to verify its authenticity using fact-checking sources.
      </p>
      <SearchBar onSearch={handleSearch} />
      {loading && <p className="loading">🔎 Checking...</p>}
      {error && <p className="error">{error}</p>}
      
      {Array.isArray(results) && results.length > 0 && (
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

