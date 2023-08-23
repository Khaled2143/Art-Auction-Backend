from dataclasses import dataclass
from main import db

@dataclass
class Artist(db.Model):
    __tablename__ = 'artist'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    email: str = db.Column(db.String(50), nullable=False)
    phone_number: str = db.Column(db.String(50), nullable=False)

    art_works = db.relationship('ArtWork', backref='artist', lazy=True)
    listings = db.relationship('Listings', backref='artist', lazy=True)