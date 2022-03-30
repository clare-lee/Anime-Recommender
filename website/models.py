from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    log = db.relationship('Log')

class Anime(db.Model):
    anime_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    genre = db.Column(db.String(45))
    medium = db.Column(db.String(45))
    episodes = db.Column(db.String(45))
    rating = db.Column(db.Float)
    ratings = db.relationship('Rating')

class Rating(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.anime_id'), primary_key=True)
    rating = db.Column(db.Integer)
    