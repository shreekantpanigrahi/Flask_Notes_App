from . import db 
from flask_login import UserMixin 
from sqlalchemy.sql import func 
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data= db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password= db.Column(db.String(150))
    firstName= db.Column(db.String(150))
    notes= db.relationship('Note')

    @property
    def is_active(self):
        return True
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except Exception as e:
            print(f"Token verification failed: {e}")
            return None
        return User.query.get(user_id)