# #!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate

from models import db, Article

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session.clear()  
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Retrieve the article
    article = Article.query.get(id)
    
    if not article:
        return jsonify({"error": "Article not found"}), 404  # Return 404 if article not found
    
    # Initialize session['page_views'] with a ternary operator
    session['page_views'] = session.get('page_views', 0) + 1
    
    # Check if the user has viewed more than 3 articles
    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401
    
    # Return the article data if the user has viewed 3 or fewer articles
    return jsonify(article.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5555)

