from flask import request, jsonify
from MVC.models import Artist
from MVC.models import ArtWork


def get_artist():
    return Artist.query.all()

def get_artwork():
    return ArtWork.query.all()

def add_artist():
    artist_data = request.get_json()
    artist = Artist(name=artist_data['name'], email=artist_data['email'], phone_number=artist_data['phone_number'])

    from MVC.models import db
    db.session.add(artist)
    db.session.commit()

    return jsonify({'message': 'Artist added successfully!'})