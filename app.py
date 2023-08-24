from flask import Flask, request, jsonify
from datetime import date
from MVC.models import Artist, ArtWork

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art_auction.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from MVC.models import db
    with app.app_context():
        db.init_app(app)
        db.create_all()

    from MVC import views
    app.add_url_rule('/artist', view_func=views.get_artist)
    app.add_url_rule('/artwork', view_func=views.get_artwork)
    app.add_url_rule('/add-artist', view_func=views.add_artist, methods=['POST'])

    return app