from flask import request, jsonify
from datetime import date
from werkzeug.utils import secure_filename
import os
from MVC.models import Artist
from MVC.models import ArtWork
from MVC.models import Buyer

def place_bid(artwork_id, buyer_id, bid_amount):
    artwork = get_artwork_by_id(artwork_id)

    if not artwork:
        return jsonify({'message': 'Artwork not found!'})
    
    buyer = get_buyer_by_id(buyer_id)

    if not buyer:
        return jsonify({'message': 'Buyer not found!'})
    
    if bid_amount <= artwork.price:
        return jsonify({'message': 'Bid amount should be greater than the current price!'})
    
    artwork.pprice = bid_amount
    artwork.buyer = buyer
    artwork.highest_bid = bid_amount


# Get Requests

def get_artist():
    return Artist.query.all()

def get_artwork():
    return ArtWork.query.all()

def get_buyer():
    return Buyer.query.all()

def get_artwork_by_id(id):
    return ArtWork.query.filter_by(id=id).first()

def get_artwork_by_artist(artist):
    return ArtWork.query.filter_by(artist=artist).all()

def get_artwork_by_title(title):
    return ArtWork.query.filter_by(title=title).all()

def get_artwork_by_price(price):
    return ArtWork.query.filter_by(price=price).all()

def get_artwork_by_creation_date(creation_date):
    return ArtWork.query.filter_by(creation_date=creation_date).all()

def get_artist_by_id(id):
    return Artist.query.filter_by(id=id).first()

def get_artist_by_name(name):
    return Artist.query.filter_by(name=name).first()

def get_buyer_by_id(id):
    return Buyer.query.filter_by(id=id).first()

def get_buyer_by_name(name):
    return Buyer.query.filter_by(name=name).first()



# Post Requests

UPLOAD_FOLDER = 'uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    artwork_data = request.form.to_dict()
    
    artist = Artist.query.filter_by(name=artwork_data['artist']).first()

    image = request.files['image']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        image.save(filepath)
        artwork_data['image'] = filepath

    artwork = ArtWork(title=artwork_data['title'],
                      artist=artist, creation_date=date.today(),
                      starting_price=artwork_data['price'], 
                      highest_bid=artwork_data['price'],
                      description=artwork_data['description'], 
                      dimension=artwork_data['dimension'], 
                      image=artwork_data['image'])

    from MVC.models import db
    db.session.add(artwork)
    db.session.commit()

    return jsonify({'message': 'Artwork added successfully!'})

# Add Buyer  
def add_buyer():
    buyer_data = request.get_json()

    buyer = Buyer(username=buyer_data['name'], email=buyer_data['email'], phone_number=buyer_data['phone_number'])
    
    from MVC.models import db
    db.session.add(buyer)
    db.session.commit()

    return jsonify({'message': 'Buyer added successfully!'})

