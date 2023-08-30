from dataclasses import dataclass
from datetime import date
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

USER_ID = 'user.id'

### ArtWork Entity
@dataclass
class ArtWork(db.Model):
    __tablename__ = 'art_work'
    id: int = db.Column(db.Integer, primary_key=True)
    creation_date: date = db.Column(db.Date, nullable=False)
    image: str = db.Column(db.String(100), nullable=False)
    title: str = db.Column(db.String(50), nullable=False)
    starting_price: float = db.Column(db.Float, nullable=False)
    current_bid: float = db.Column(db.Float, nullable=False)
    available: bool = db.Column(db.Boolean, nullable=False)
    end_time: date = db.Column(db.DateTime, nullable=False)
    end_date: date = db.Column(db.Date, nullable=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey(USER_ID), nullable=False)
    current_bidder_id: int = db.Column(db.Integer, db.ForeignKey(USER_ID))



### User Entity
@dataclass
class User(db.Model):
    __tablename__ = 'user'
    id: int = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email: str = db.Column(db.String(50), nullable=False)
    phone_number: str = db.Column(db.String(50), nullable=False)

    art_works = db.relationship('ArtWork', backref='user', lazy=True, foreign_keys=[ArtWork.user_id])
    bidded_art_works = db.relationship('ArtWork', backref='current_bidder', lazy=True, foreign_keys=[ArtWork.current_bidder_id])
    purchases = db.relationship('Purchase', backref='user', lazy=True)


### Purchase Entity
@dataclass
class Purchase(db.Model):
    __tablename__= 'purchase'
    id = db.Column(db.Integer,primary_key=True)
    title: str = db.Column(db.String(50), db.ForeignKey('art_work.title'), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_price: float = db.Column(db.Float, nullable=False)
    artwork_id: int = db.Column(db.Integer, db.ForeignKey('art_work.id'), nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey(USER_ID), nullable=False)
