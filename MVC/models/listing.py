from dataclasses import dataclass
from main import db

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

