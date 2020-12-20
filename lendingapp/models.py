from lendingapp.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    borrowing_limit = db.Column(db.Integer, default=3)
