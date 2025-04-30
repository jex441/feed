from app.fetch_news import fetch_news
from app.summarize_article import process_request
from app import db, app, Article
import schedule 
import time 

def get_data():
    print('getting data')
    raw_articles = fetch_news()

    articles = []
    for item in raw_articles:
        with app.app_context():  # Create application context for database operations
            duplicate = Article.query.filter_by(url=item.get("url")).first()
            if duplicate is None:
                article_summary = process_request(item)
                if article_summary is not None:
                    articles.append({"title": article_summary.headline, "image": item.get("image"), "description": article_summary.description, "content": article_summary.summary, "url": item.get("url"), "source": item.get("source")})
 
    # create new message entry in db with response
    with app.app_context():  # Create application context for database operations
        for item in articles:
            new_article = Article(title=item.get("title"), description=item.get("description"), content=item.get("content"), image=item.get("image"), author=item.get("author"), url=item.get("url"), source=item.get("source"))
            db.session.add(new_article)
            db.session.commit()
    
    print('articles added')
