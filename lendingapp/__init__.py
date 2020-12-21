import os

from flask import Flask

from lendingapp import db, api
from .api import UserBorrowedBooks, Books, Checkouts
from .api import Book as BookResource
from .models import User, Book, Checkout

######################################
#### Application Factory Function ####
######################################
def create_app(config_filename="lendingapp.cfg"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


##########################
#### Helper Functions ####
##########################
def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_db(app)
    restful_api = api.init_app(app)
    register_endpoints(restful_api)


def register_endpoints(api):
    api.add_resource(UserBorrowedBooks, "/api/users/<int:user_id>/books")
    api.add_resource(Books, "/api/books")
    api.add_resource(BookResource, "/api/book/<int:book_id>")
    api.add_resource(Checkouts, "/api/checkouts")
