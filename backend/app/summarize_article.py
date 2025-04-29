import requests
from typing import List, Dict
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
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
                "content": f"summarize this article in one sentence in a casual tone.",
            },
            {"role": "user", "content": raw_article_content},
        ],
        response_format=ArticleExtraction,
    )
    result = completion.choices[0].message.parsed
    return result

def process_request(article):
    # First LLM call: Extract basic info
    initial_extraction = extract_article(article["title"])

    # Gate check: Verify if it's an outcome related to a job recruiter
    if (
        not initial_extraction.is_valid_article
        or initial_extraction.confidence_score < 0.7
    ):
        return None

    article_summary = summarize_article(article["content"])
    return article_summary
