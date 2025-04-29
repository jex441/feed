import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_KEY = os.getenv("API_KEY")
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"

def fetch_news(query: str, page_size: int = 1) -> List[Dict]:
    headers = {
        "Authorization": NEWSAPI_KEY
    }
    params = {
        "q": query,
        "pageSize": page_size,
        "sortBy": "publishedAt",  # Sort by newest first
        "language": "en",
        "sources": ["associated-press", "the-new-york-times, the-wall-street-journal"]
    }
    
    response = requests.get(NEWSAPI_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad responses

    data = response.json()

    articles = []
    for item in data.get("articles", []):
        articles.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "description": item.get("description"),
            "source": item.get("source", {}).get("name", "Unknown"),
            "publishedAt": item.get("publishedAt"),
            "content": item.get("content"),
            "image": item.get("urlToImage")
        })

    return articles