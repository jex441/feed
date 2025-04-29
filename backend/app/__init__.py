from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True
     }})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helix.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    url = db.Column(db.Text())
    image = db.Column(db.Text())
    author = db.Column(db.Text())
    source = db.Column(db.Text())
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "image": self.image,
            "author": self.author,
            "source": self.source,
            "date_created": self.date_created
        }


from app import routes  # Import routes after creating app
