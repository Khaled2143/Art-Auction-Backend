from dataclasses import dataclass
from main import db

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