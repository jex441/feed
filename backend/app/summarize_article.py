import requests
from typing import List, Dict
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o"


class ArticleExtraction(BaseModel):
    description: str = Field(description="Raw description of the article")
    is_valid_article: bool = Field(
        description="Whether this text is a quality article and not clickbait."
    )
    confidence_score: float = Field(description="Confidence score between 0 and 1")

class ArticleSummary(BaseModel):
    summary: str = Field(
        description="A very concise summary of the article in a neutral tone."
    )
    headline: str = Field(description="A very concise headline of the article.")

def extract_article(title: str) -> ArticleExtraction:
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are a journalism expert. Analyze the headline of this article and determine if it is a quality article and not clickbait.",
            },
            {"role": "user", "content": title},
        ],
        response_format=ArticleExtraction,
    )
    result = completion.choices[0].message.parsed
    return result

def summarize_article(raw_article_content: str) -> ArticleSummary:
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"summarize this article in one sentence in a casual tone. your response should be in two parts, the content and a very short title for the article.",
            },
            {"role": "user", "content": raw_article_content},
        ],
        response_format=ArticleSummary,
    )
    result = completion.choices[0].message.parsed
    return result

def fetch_article_content(url: str) -> str:
    """Fetch and extract the main content from an article URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Use BeautifulSoup to parse and extract content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        text = ' '.join(line for line in lines if line)
        
        return text
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return ""

def process_request(article):
    # First LLM call: Extract basic info
    initial_extraction = extract_article(article["title"])

    # Gate check: Verify if it's an outcome related to a job recruiter
    if (
        not initial_extraction.is_valid_article
        or initial_extraction.confidence_score < 0.7
    ):
        print("not valid article", article["title"], initial_extraction.confidence_score)
        return None
    
    # Try to get full article content from URL if available
    content_text = ""
    if article.get("url"):
        print(f"Fetching content from URL: {article['url']}")
        content_text = fetch_article_content(article["url"])
    
    # If URL fetching failed or no URL provided, fall back to snippet
    if not content_text:
        if article["content"] is None:
            # Use description or title as fallback
            content_text = article.get("description") or article.get("title") or ""
        else:
            content_text = article["content"]
    
    article_summary = summarize_article(content_text)
    print(article_summary)

    return article_summary
