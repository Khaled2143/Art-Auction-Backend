from dataclasses import dataclass
from datetime import datetime
from main import db

@dataclass
class ArtWork(db.Model):
    __tablename__ = 'art_work'
    id: int = db.Column(db.Integer, primary_key=True)
    creation_date: datetime = db.Column(db.Date, nullable=False)
    dimensions: str = db.Column(db.String(50), nullable=False)
    description: str = db.Column(db.String(500), nullable=False)
    image: str = db.Column(db.String(100), nullable=False)
    title: str = db.Column(db.String(50), nullable=False)
    price: float = db.Column(db.Float, nullable=False)
    artist_id: int = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    
    #make get_art_work_by_id() method