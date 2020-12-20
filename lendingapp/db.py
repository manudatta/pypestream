from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    Migrate(app, db)


def get_db():
    if "db" not in g:
        g.db = db
    return g.db
