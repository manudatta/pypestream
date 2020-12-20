import sqlite3

from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def get_db():
    if "db" not in g:
        g.db = db
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
