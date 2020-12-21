import datetime

from flask_restful import Resource, Api, abort
from flask_restful import reqparse

from . import models
from .db import db
from .models import User, Checkout,  checkout
from .models import Book as BookModel


def init_app(app):
    api = Api(app)
    return api
# List the book a user has checked out
class UserBorrowedBooks(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        borrowed_books = [book.to_json() for book in user.borrowed_books]
        return {'borrowed_books':borrowed_books}
# List all the books with upcoming due dates
class Books(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('is_due', type=int, location='args')
        args = parser.parse_args()
        if args.get('is_due') != 1:
            return abort(400,message='only due date serach is valid so far')
        checkouts = Checkout.query.filter(Checkout.due_at >= datetime.date.today())
        books = [c.book.to_json() for c in checkouts]
        return {'books':books}

# Delete book(s)
class Book(Resource):
    def delete(self, book_id):
        try:
            book = BookModel.query.get(book_id)
            book_json = book.to_json()
            db.session.delete(book)
            db.session.commit()
            return {'book':book_json}
        except :
            return abort(204,message=f" not found book with id:{book_id}")


# Let user checkout an available book if quota permits
class Checkouts(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, location='form')
        parser.add_argument('book_id', type=int, location='form')
        args = parser.parse_args()
        if args.get('user_id') is None or args.get('book_id') is None:
            return abort(400,message='missing user_id or book_id for checkout')
        try:
            user_id = args['user_id']
            book_id = args['book_id']
            user = User.query.get(user_id)
            book = BookModel.query.get(book_id)
            checkout = models.checkout(user,book)
            return {'checkout': checkout.to_json()}
        except Exception as e:
            return abort(400,message=str(e))
