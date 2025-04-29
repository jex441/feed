from flask import request, jsonify
from app import app
from app.fetch_news import fetch_news
from app.summarize_article import process_request
from app import db
from app import Article

@app.route('/api/news', methods=['POST', 'GET'])
def get_news():
    if request.method == 'POST':
        topic = request.args.get('topic', 'general')
        raw_articles = fetch_news(topic)
    
        articles = []
        for item in raw_articles:
            duplicate = Article.query.filter_by(url=item.get("url")).first()
            if duplicate is None:
                article_summary = process_request(item)
                if article_summary is not None:
                    articles.append({"title": article_summary.headline, "image": item.get("image"), "description": article_summary.description, "content": article_summary.summary, "url": item.get("url"), "source": item.get("source")})
 
        # create new message entry in db with response
        for item in articles:
            new_article = Article(title=item.get("title"), description=item.get("description"), content=item.get("content"), image=item.get("image"), author=item.get("author"))
            db.session.add(new_article)
            db.session.commit()

        return jsonify(articles)

    elif request.method == 'GET':
        articles = Article.query.order_by(Article.date_created.desc()).all()
        aricles_dict = [art.to_dict() for art in articles]
        feed = jsonify(aricles_dict)
        return feed