from flask import Flask
from flask_cors import CORS
import secrets



def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art_auction.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from MVC.models import db
    with app.app_context():
        db.init_app(app)
        db.create_all()

    from MVC import views

    app.add_url_rule('/users', view_func=views.get_user)
    app.add_url_rule('/users'/{id}, view_func=views.get_user)
    app.add_url_rule('/users/user/{username}', view_func=views.get_user)
    app.add_url_rule('/artworks', view_func=views.get_artwork)
    app.add_url_rule('/artworks/{id}', view_func=views.get_artwork)
    app.add_url_rule('/artworks/title/{title}', view_func=views.get_artwork)
    app.add_url_rule('/artworks/user/{username}', view_func=views.get_artwork)
    app.add_url_rule('/artworks/date/{creation_date}', view_func=views.get_artwork)
    app.add_url_rule('/artworks/price/{price}', view_func=views.get_artwork)
    app.add_url_rule('/purchases', view_func=views.get_purchases)
    app.add_url_rule('/purchases/{id}', view_func=views.get_purchases)
    app.add_url_rule('/add-user', view_func=views.add_user, methods=['POST'])
    app.add_url_rule('/add-artwork', view_func=views.add_artwork, methods=['POST'])
    app.add_url_rule('/place-bid/<artwork_id>/<buyer_id>/<bid_amount>', view_func=views.place_bid, methods=['POST']) ## Change based on frontend
    app.add_url_rule('/login', view_func=views.login_user, methods=['POST'])
    app.add_url_rule('/logout', view_func=views.logout_user, methods=['POST'])

    return app