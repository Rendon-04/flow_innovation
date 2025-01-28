import React, { useState } from 'react';
import './SearchBar.css';

const SearchBar = ({ onSearch }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSearch(input);
    }
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        className="search-input"
        placeholder="Enter a claim to fact-check..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button type="submit" className="search-button">Search</button>
    </form>
  );
};

export default SearchBar;
