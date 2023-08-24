from dataclasses import dataclass
from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

@dataclass
class ArtWork(db.Model):
    __tablename__ = 'art_work'
    id: int = db.Column(db.Integer, primary_key=True)
    creation_date: date = db.Column(db.Date, nullable=False)
    dimension: str = db.Column(db.String(50), nullable=False)
    description: str = db.Column(db.String(500), nullable=False)
    image: str = db.Column(db.String(100), nullable=False)
    title: str = db.Column(db.String(50), nullable=False)
    starting_price: float = db.Column(db.Float, nullable=False)
    current_bid: float = db.Column(db.Float, nullable=False)
    artist_id: int = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    #make get_art_work_by_id() method

@dataclass
class Artist(db.Model):
    __tablename__ = 'artist'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    email: str = db.Column(db.String(50), nullable=False)
    phone_number: str = db.Column(db.String(50), nullable=False)

    art_works = db.relationship('ArtWork', backref='artist', lazy=True)


@dataclass
class Buyer(db.Model):
    __tablename__ = 'buyer'
    buyer_id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), nullable=False)
    email: str = db.Column(db.String(50), nullable=False)
    phone_number: str = db.Column(db.String(50), nullable=False)



class Guest:
    SessionID: str