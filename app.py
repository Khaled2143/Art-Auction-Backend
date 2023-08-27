from flask import Flask
from flask_cors import CORS
import secrets

def create_app():
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art_auction.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from MVC.models import db
    with app.app_context():
        db.init_app(app)
        db.create_all()

    from MVC import views

    app.add_url_rule('/users', view_func=views.get_users)
    app.add_url_rule('/users/<username>', view_func=views.get_user_by_username)
    app.add_url_rule('/artworks', view_func=views.get_artwork)
    app.add_url_rule('/artworks/featured', view_func=views.get_featured_artwork)
    app.add_url_rule('/artworks/<id>', view_func=views.get_artwork_by_id)
    app.add_url_rule('/images/<image_filename>', view_func=views.get_image)
    app.add_url_rule('/purchases', view_func=views.get_purchases)
    app.add_url_rule('/add-user', view_func=views.add_user, methods=['POST'])
    app.add_url_rule('/add-artwork', view_func=views.add_artwork, methods=['POST'])
    app.add_url_rule('/place-bid/<artwork_id>', view_func=views.place_bid, methods=['POST']) ## Change based on frontend
    app.add_url_rule('/login', view_func=views.login, methods=['POST'])
    app.add_url_rule('/logout', view_func=views.logout, methods=['POST'])
    app.add_url_rule('/check-auth', view_func=views.check_auth, methods=['POST'])

    return app