import React from 'react';
import './NewsCard.css';

const NewsCard = ({ article }) => {
  return (
    <div className="news-card">
      {article.urlToImage && <img src={article.urlToImage} alt={article.title} className="news-image" />}
      <div className="news-content">
        <h2 className="news-title">{article.title}</h2>
        <p className="news-description">{article.description}</p>
        <a href={article.url} target="_blank" rel="noopener noreferrer" className="news-link">
          Read More
        </a>
      </div>
    </div>
  );
};

export default NewsCard;
