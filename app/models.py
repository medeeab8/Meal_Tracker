from . import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)
