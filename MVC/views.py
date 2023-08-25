from flask import request, session, jsonify
import os
from datetime import date
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


from MVC.models import ArtWork
from MVC.models import User
from MVC.models import Purchase
from MVC.models import db

def place_bid(artwork_id, user_id, bid_amount):

    if not session.get('username'):
        return jsonify({'message': 'You need to be logged in to place a bid!'})

    artwork = get_artwork_by_id(artwork_id)

    if not artwork:
        return jsonify({'message': 'Artwork not found!'})

    user = get_user_by_id(user_id)

    if artwork.user == user:
        return jsonify({'message': 'You cannot bid on your own artwork!'})

    bid_amount = float(bid_amount)

    if bid_amount <= artwork.current_bid:
        return jsonify({'message': 'Bid amount should be greater than the current price!'})
    
    prev_Winner = None
    if artwork.current_bidder_id:
        prev_Winner = get_user_by_id(artwork.current_bidder_id)
    
    if prev_Winner:
        prev_purchase = Purchase.query.filter_by(artwork_id=artwork_id, user_id=prev_Winner.id).first()
        if prev_purchase:
            db.session.delete(prev_purchase)
    
    purchase = Purchase(title=artwork.title, user=user, purchase_date=date.today(), purchase_price=bid_amount, artwork_id=artwork_id)
    user.purchases.append(purchase)
    artwork.current_bid = bid_amount
    artwork.current_bidder_id = user_id
    db.session.commit()

    return jsonify({'message': 'Bid placed successfully!'})

# login request

def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # loads user 
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        response = {"message": "Login successful"}
        session['username'] = user.username # Store the username in the session
        return jsonify(response), 200
    else:
        response = {"message": "Invalid credentials"}
        return jsonify(response), 401
    
def logout():
    session.pop('username', None)
    return jsonify({"message": "Logout successful"}), 200



# Get Requests

def get_user():
    return User.query.all()

def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_artwork():
    return ArtWork.query.all()

def get_artwork_by_id(id):
    return ArtWork.query.filter_by(id=id).first()

def get_artwork_by_user(username):
    return ArtWork.query.filter_by(username=username).all()

def get_artwork_by_title(title):
    return ArtWork.query.filter_by(title=title).all()

def get_artwork_by_price(price):
    return ArtWork.query.filter_by(price=price).all()

def get_artwork_by_creation_date(creation_date):
    return ArtWork.query.filter_by(creation_date=creation_date).all()

def get_purchases():
    return Purchase.query.all()

def get_purchase_by_id():
    return Purchase.query.filter_by(id=id).first()

# def get_purchases_by_date()



# Post Requests

UPLOAD_FOLDER = 'uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add Artwork
def add_artwork():

    if not session.get('username'):
        return jsonify({'message': 'You need to be logged in to add an artwork!'})
    artwork_data = request.form.to_dict()
    
    user = User.query.filter_by(name=artwork_data['user']).first()

    image = request.files['image']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        image.save(filepath)
        artwork_data['image'] = filepath

    artwork = ArtWork(title=artwork_data['title'],
                      user=user, creation_date=date.today(),
                      starting_price=artwork_data['price'],
                      current_bid=artwork_data['price'],
                      image=artwork_data['image'])
    db.session.add(artwork)
    db.session.commit()

    return jsonify({'message': 'Artwork added successfully!'})



# Add User
def add_user():
    user_data = request.get_json()

    # check if the  username is in the database
    user = User.query.filter_by(name=user_data['user']).first()
   
    if user:
        return jsonify({"message": "This username is already in use"}), 400

    # check if the email is in the database
    email = User.query.filter_by(email=user_data['email']).first()
    if email:
        return jsonify({"message": "This email is already in use"}), 400

    password = user_data['password']
    hashed_password = generate_password_hash(password)  # Hash the password

    new_user = User(username=user_data['username'], password_hash=hashed_password, email=user_data['email'], phone_number=user_data['phone_number'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


