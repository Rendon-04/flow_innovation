import React, { useEffect, useState } from 'react';
import NewsCard from './NewsCard';
import './InnovationNewsPage.css';

const InnovationNewsPage = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/innovation_news')
      .then(response => response.json())
      .then(data => {
        if (data.articles) {
          setArticles(data.articles);
        } else {
          setError('Failed to fetch news articles');
        }
        setLoading(false);
      })
      .catch(err => {
        setError('Error fetching news');
        setLoading(false);
      });
  }, []);

  return (
    <div className="innovation-news-container">
      <h1 className="page-title">Innovation News</h1>
      {loading && <p className="loading">Loading...</p>}
      {error && <p className="error">{error}</p>}
      <div className="news-grid">
        {articles.map((article, index) => (
          <NewsCard key={index} article={article} />
        ))}
      </div>
    </div>
  );
};

export default InnovationNewsPage;
