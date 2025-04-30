from flask import request, jsonify
from app import app
from app.fetch_news import fetch_news
from app.summarize_article import process_request
from app import db
from app import Article

@app.route('/api/news', methods=['GET'])
def get_news():
    articles = Article.query.order_by(Article.date_created.desc()).all()
    articles_dict = [art.to_dict() for art in articles]
    feed = jsonify(articles_dict)
    return feed