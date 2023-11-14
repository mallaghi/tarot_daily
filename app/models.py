from app import db

class User(db.Model):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    subscribed = db.Column(db.Boolean, default=True)
