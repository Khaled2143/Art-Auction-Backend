from flask import request, send_from_directory, session, jsonify
import os
from datetime import date, datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


from MVC.models import ArtWork
from MVC.models import User
from MVC.models import Purchase
from MVC.models import db

def place_bid(artwork_id):

    if not session.get('username'):
        return jsonify({'message': 'You need to be logged in to place a bid!'}), 401

    artwork = get_artwork_by_id(artwork_id)

    if not artwork.available:
        return jsonify({'message': 'Auction is closed!'}), 400

    data = request.get_json()
    bid_amount = data.get('bid_amount')

    if not artwork:
        return jsonify({'message': 'Artwork not found!'}), 404

    user = get_user_by_username(session.get('username'))

    if artwork.user == user:
        return jsonify({'message': 'You cannot bid on your own artwork!'}), 400

    bid_amount = float(bid_amount)

    if bid_amount <= artwork.current_bid:
        return jsonify({'message': 'Bid amount should be greater than the current price!'}), 400
    
    prev_winner = None
    if artwork.current_bidder_id:
        prev_winner = get_user_by_id(artwork.current_bidder_id)
    
    if prev_winner:
        prev_purchase = Purchase.query.filter_by(artwork_id=artwork_id, user_id=prev_winner.id).first()
        if prev_purchase:
            db.session.delete(prev_purchase)
    
    purchase = Purchase(title=artwork.title, user=user, purchase_date=date.today(), purchase_price=bid_amount, artwork_id=artwork_id)
    user.purchases.append(purchase)
    artwork.current_bid = bid_amount
    artwork.current_bidder_id = user.id
    db.session.commit()

    return jsonify({'message': 'Bid placed successfully!'}), 200


### Get Requests

def get_users():
    users = User.query.all()

    # Convert user instances to a list of dictionaries
    users_list = []
    for user in users:
        user_dict = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number
            # Add more attributes as needed
        }
        users_list.append(user_dict)
    return users_list

def get_user_by_id(id):
    
    return User.query.filter_by(id=id).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_artworks():
    art_works = ArtWork.query.filter_by(available=True).all()

    # Convert user instances to a list of dictionaries
    art_works_list = []
    for art_work in art_works:
        art_work_dict = {
            'id': art_work.id,
            'image': art_work.image,
        }
        art_works_list.append(art_work_dict)

    return art_works_list, 200

def get_all_artworks():
    art_works = ArtWork.query.all()
    return art_works

def get_featured_artwork():
    art_works = ArtWork.query.all()

    # Convert user instances to a list of dictionaries
    art_works_list = []
    for art_work in art_works:
        art_work_dict = {
            'id': art_work.id,
            'image': art_work.image,
        }
        art_works_list.append(art_work_dict)

    return art_works_list[:4], 200

def get_artwork_by_id(id):
    artwork = ArtWork.query.filter_by(id=id).first()
    if not artwork:
        return jsonify({'message': 'Artwork not found!'}), 404
    
    user = get_user_by_id(artwork.user_id)

    remaining_time = artwork.end_time - datetime.now()
    remaining_seconds = max(remaining_time.total_seconds(), 0)
    
    artwork_dict = {
        'id': artwork.id,
        'title': artwork.title,
        'creation_date': artwork.creation_date,
        'image': artwork.image,
        'current_bid': artwork.current_bid,
        'artist_name': user.username,
        'available': artwork.available,
        'remaining_time': remaining_seconds,
    }

    return artwork_dict, 200

def get_image(image_filename):
    return send_from_directory('uploaded_images', image_filename)

def get_artwork_by_creation_date(creation_date):
    return ArtWork.query.filter_by(creation_date=creation_date).all()

def get_purchases():
    if not session.get('username'):
        return jsonify({'message': 'You need to be logged in to view purchases!'}), 401
    return Purchase.query.all()

def get_purchase_by_id():
    return Purchase.query.filter_by(id=id).first()

### Post Requests

def check_auth():
    if 'username' in session and session['username'] != '':
        print(session['username'])
        return jsonify({'authenticated': True}), 200
    else:
        print('not authenticated')
        return jsonify({'authenticated': False}), 200


### login request

def login():
    data = request.form.to_dict()
    username = data.get('username')
    password = data.get('password')

    # loads user 
    user = get_user_by_username(username)

    if not user:
        user = get_user_by_email(username)

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

### Add Artwork

UPLOAD_FOLDER = 'uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_artwork():

    if not session.get('username'):
        return jsonify({'message': 'You need to be logged in to add an artwork!'}), 401
    
    username = session.get('username')

    artwork_data = request.form.to_dict()
    
    user = get_user_by_username(username)

    image = request.files['image']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        image.save(filepath)

        image_url = request.url_root + 'images/' + filename
        artwork_data['image'] = image_url

    end_time = datetime.now() + timedelta(minutes=5)

    artwork = ArtWork(title=artwork_data['title'],
                      user=user, creation_date=date.today(),
                      starting_price=artwork_data['price'],
                      current_bid=artwork_data['price'],
                      image=artwork_data['image'], 
                      available=True, end_time=end_time)
    db.session.add(artwork)
    db.session.commit()

    return jsonify({'message': 'Artwork added successfully!'}), 201



### Add User
def add_user():
    user_data = request.form.to_dict()

    # check if the  username is in the database
    user = User.query.filter_by(username=user_data['username']).first()
   
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



### misc

