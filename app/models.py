from . import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    height = db.Column(db.Integer, nullable=False)  # height in cm
    weight = db.Column(db.Integer, nullable=False)  # weight in kg
    activity_level = db.Column(db.Integer, nullable=False)  # activity level from 1 to 5
    tdee = db.Column(db.Integer, nullable=True)