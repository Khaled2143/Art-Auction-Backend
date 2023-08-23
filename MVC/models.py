from dataclasses import dataclass
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

@dataclass
class ArtWork(db.Model):
    __tablename__ = 'art_work'
    id: int = db.Column(db.Integer, primary_key=True)
    creation_date: datetime = db.Column(db.Date, nullable=False)
    dimension: str = db.Column(db.String(50), nullable=False)
    description: str = db.Column(db.String(500), nullable=False)
    image: str = db.Column(db.String(100), nullable=False)
    title: str = db.Column(db.String(50), nullable=False)
    price: float = db.Column(db.Float, nullable=False)
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
    listings = db.relationship('Listings', backref='artist', lazy=True)


@dataclass
class Buyer(db.Model):
    __tablename__ = 'buyer'
    buyer_id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), nullable=False)
    email: str = db.Column(db.String(50), nullable=False)
    addressLine1: str = db.Column(db.String(50), nullable=False)
    addressLine2: str = db.Column(db.String(50), nullable=True)
    city: str = db.Column(db.String(50), nullable=False)
    state: str = db.Column(db.String(50), nullable=False)
    zipcode: str = db.Column(db.String(50), nullable=False)


@dataclass
class Listings(db.Model):
    __tablename__ = 'listing'
    id: str = db.Column(db.Integer, primary_key=True)
    artist_id: int = db.Column(db.Integer, db.ForeignKey('artist.id')) #FK to seller model (table)
    title: str = db.Column(db.String(100))
    image: str = db.Column(db.String(100)) #may use BLOB datatype
    price: int = db.Column(db.Integer)
    description: str = db.Column(db.String(1000))
    listing_date: str = db.Column(db.String(100))
    art_work_id: int = db.Column(db.Integer, db.ForeignKey('art_work.id')) #FK to art_work model (table)


class Guest:
    SessionID: str