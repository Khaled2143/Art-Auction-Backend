from main import app, db
from MVC.models.artist import Artist
from MVC.models.art_work import ArtWork
from datetime import datetime

artist = Artist(name='Pablo Picasso', email='example@123.com', phone='1234567890')
art_work = ArtWork(title='The Old Guitarist', 
                    creation_date=datetime(1405, 11, 5), 
                    artist_id=artist, 
                    price=1000000, description='This is a description', dimension='10X10', image='image', )

artist.art_works.append(art_work)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
    
        db.session.add(artist)
        db.session.commit()