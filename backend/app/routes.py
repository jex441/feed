from flask import request, jsonify
from app import app
from app.fetch_news import fetch_news
from app.summarize_article import process_request

@app.route('/api/news', methods=['GET'])
def get_news():
    topic = request.args.get('topic', 'general')
    raw_articles = fetch_news(topic)
    articles = []
    for item in raw_articles:
        article_summary = process_request(item)
        article_summary = "der"
        articles.append({"title": item.get("title"), "image": item.get("image"), "content": article_summary})

    return jsonify(articles)