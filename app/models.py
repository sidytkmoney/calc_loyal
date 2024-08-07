# app/models.py
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    loyalties = db.relationship('Loyalty', backref='author', lazy=True)

class Loyalty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name1 = db.Column(db.String(50), nullable=False)
    name2 = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
