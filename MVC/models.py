from dataclasses import dataclass
from datetime import date
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

@dataclass
class ArtWork(db.Model):
    __tablename__ = 'art_work'
    id: int = db.Column(db.Integer, primary_key=True)
    creation_date: date = db.Column(db.Date, nullable=False)
    image: str = db.Column(db.String(100), nullable=False)
    title: str = db.Column(db.String(50), nullable=False)
    starting_price: float = db.Column(db.Float, nullable=False)
    current_bid: float = db.Column(db.Float, nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    current_bidder_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))

    #make get_art_work_by_id() method

@dataclass
class User(db.Model):
    __tablename__ = 'user'
    id: int = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email: str = db.Column(db.String(50), nullable=False)
    phone_number: str = db.Column(db.String(50), nullable=False)

    art_works = db.relationship('ArtWork', backref='user', lazy=True)
    purchases = db.relationship('Purchase', backref='user', lazy=True)

@dataclass
class Purchase(db.Model):
    __tablename__= 'purchase'
    id = db.Column(db.Integer,primary_key=True)
    title: str = db.Column(db.String(50), db.ForeignKey('artwork.title'), nullable=False)
    purchase_date = db.Column(db.DateTime, default = date.utcnow, nullable=False)
    purchase_price: float = db.Column(db.Float, nullable=False)
    artwork_id: int = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
