from flask import request, jsonify
from datetime import date
from MVC.models import Artist
from MVC.models import ArtWork


def get_artist():
    return Artist.query.all()

def get_artwork():
    return ArtWork.query.all()


# Post Requests

# Add Artist
def add_artist():
    artist_data = request.get_json()
    artist = Artist(name=artist_data['name'], email=artist_data['email'], phone_number=artist_data['phone_number'])

    from MVC.models import db
    db.session.add(artist)
    db.session.commit()

    return jsonify({'message': 'Artist added successfully!'})

# Add Artwork
def add_artwork():
    artwork_data = request.get_json()
    
    artist = Artist.query.filter_by(name=artwork_data['artist']).first()

    artwork = ArtWork(title=artwork_data['title'],
                      artist=artist, creation_date=date.today(),
                      price=artwork_data['price'], 
                      description=artwork_data['description'], 
                      dimension=artwork_data['dimension'], 
                      image=artwork_data['image'])

    from MVC.models import db
    db.session.add(artwork)
    db.session.commit()

    return jsonify({'message': 'Artwork added successfully!'})