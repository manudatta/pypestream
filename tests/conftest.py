import os
import tempfile

import pytest
from faker import Faker

from lendingapp import create_app, User
from lendingapp.db import get_db, init_db


@pytest.fixture
def app():

    app = create_app("lendingapp_test.cfg")

    with app.app_context():
        init_db(app)

    yield app


@pytest.fixture
def db(app):
    with app.app_context():
        init_db(app)
        test_db = get_db()
        test_db.create_all()
        yield test_db


@pytest.fixture
def new_user(db):
    faker = Faker()
    fake_name = faker.name()
    user = User(name=fake_name)
    db.session.add(user)
    db.session.flush()
    return user


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
