"""
Defining the user model
"""
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(64), unique=True, nullable=True)
    last_public_id_created = db.Column(db.DateTime, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    api_token = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    user_apis = db.relationship('Api', back_populates='user')
    

    def __str__(self):
        return f'User(id={self.id}, email={self.email}, public_id={self.public_id})'
