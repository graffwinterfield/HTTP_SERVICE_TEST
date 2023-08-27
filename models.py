from flask_login import UserMixin
from __init__ import db
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class File(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), default=datetime.utcnow().strftime('%m.%d.%Y %H:%M:%S'))

    def __repr__(self):
        return '<Article %r>' % self.id
