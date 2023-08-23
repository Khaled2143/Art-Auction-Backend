from flask import Flask, session 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from MVC.models.art_work import ArtWork
from MVC.models.artist import Artist


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art_auction.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def hello():
    return Artist.query.all()



# @app.route('/guest', methods = ['GET'])
# def getSessionId():
#     session_id: session.get("id")
#     return session_id
