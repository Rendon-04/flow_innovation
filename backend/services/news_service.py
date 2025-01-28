import requests
from flask import current_app

class NewsService:
    def __init__(self, api_key=None):
        # If no API key is provided, fetch from app's config
        self.api_key = api_key or current_app.config["NEWS_API_KEY"]
        self.base_url = "https://newsapi.org/v2/everything"

    def _fetch_news(self, query="innovation", language="en", page_size=5):
        """
        A private method that performs the actual API request to NewsAPI.
        """
        url = f"{self.base_url}?q={query}&apiKey={self.api_key}&language={language}&pageSize={page_size}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log and return the error
            current_app.logger.error(f"Error fetching news: {str(e)}")
            return {"error": str(e)}

    def get_innovation_articles(self, query="innovation", language="en", page_size=5):
        """
        Public method to fetch innovation-related news articles.
        """
        result = self._fetch_news(query, language, page_size)
        if "error" in result:
            return {"error": "Failed to fetch innovation news."}  # You can customize this error message
        return result.get("articles", [])