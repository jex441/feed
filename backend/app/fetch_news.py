import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_KEY = os.getenv("API_KEY")
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/top-headlines"

def fetch_news(page_size: int = 20) -> List[Dict]:
    headers = {
        "Authorization": NEWSAPI_KEY
    }
    params = {
       # "q": query,
        "pageSize": page_size,
        #"sortBy": "publishedAt",  # Sort by newest first
        #"language": "en",
        #"country": "us",
        "sources": "the-new-york-post,bbc-news,the-guardian-uk,the-times-of-india,the-wall-street-journal,the-new-york-times,the-economist,the-hindu,the-washington-post,the-washington-times,the-new-york-times,the-economist,the-hindu,the-washington-post,the-washington-times"
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
            "image": item.get("urlToImage"),
            "source": item.get("source", {}).get("name", "Unknown"),
        })

    return articles