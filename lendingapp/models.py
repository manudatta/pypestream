from lendingapp.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    borrowing_limit = db.Column(db.Integer, default=3)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    genre = db.Column(db.Text)


#    Checkouts: User; ID, Book; ID, Date and Due; Date
