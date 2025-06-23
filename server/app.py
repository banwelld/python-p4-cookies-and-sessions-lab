#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    response_body = [
        article.to_dict(only = ('id', 'title', 'preview', 'minutes_to_read', 'date'))
        for article in articles
    ]
    return make_response(response_body, 200)
    

@app.route('/articles/<int:id>')
def show_article(id):
    views = session.get('page_views') or 0
    views += 1
    
    session['page_views'] = views
    
    if views > 3:
        return make_response({'message': 'Maximum pageview limit reached'}, 401)
    
    article = Article.query.filter_by(id=id).first()
    
    if not article:
        return make_response({'error': f'Article {id} was not found.'}, 404)
    
    response_body = article.to_dict()
    
    return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
