from flask import Flask, session
from datetime import datetime
from MVC.models import Artist, ArtWork

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art_auction.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from MVC.models import db
    with app.app_context():
        db.init_app(app)

        artist = Artist(name='Pablo Picasso', email='example@123.com', phone_number='1234567890')
        art_work = ArtWork(title='The Old Guitarist', 
                        creation_date=datetime(1405, 11, 5), 
                        artist_id=artist, 
                        price=1000000, description='This is a description', dimension='10X10', image='image', )

        artist.art_works.append(art_work)
        db.create_all()
        db.session.add(artist)
        db.session.commit()

    from MVC import views
    app.add_url_rule('/', view_func=views.home)

    return app