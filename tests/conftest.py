import random

import pytest
from faker import Faker

from lendingapp import create_app, User, Book, models
from lendingapp.db import get_db, init_db

TOP_LEVEL_GENRE_CLASSIFICATION = ["Fiction", "Nonfiction"]
GENRE_DICT = {
    TOP_LEVEL_GENRE_CLASSIFICATION[0]: [
        "Action and adventure",
        "Alternate history",
        "Anthology",
        "Chick lit",
        "Children's",
        "Classic",
        "Comic book",
        "Coming-of-age",
        "Crime",
        "Drama",
        "Fairytale",
        "Fantasy",
        "Graphic novel",
        "Historical fiction",
        "Horror",
        "Mystery",
        "Paranormal romance",
        "Picture book",
        "Poetry",
        "Political thriller",
        "Romance",
        "Satire",
        "Science fiction",
        "Short story",
        "Suspense",
        "Thriller",
        "Western",
        "Young adult",
    ],
    TOP_LEVEL_GENRE_CLASSIFICATION[1]: [
        "Action and adventure",
        "Art/architecture",
        "Autobiography",
        "Biography",
        "Business/economics",
        "Crafts/hobbies",
        "Cookbook",
        "Diary",
        "Dictionary",
        "Encyclopedia",
        "Guide",
        "Health/fitness",
        "History",
        "Home and garden",
        "Humor",
        "Journal",
        "Math",
        "Memoir",
        "Philosophy",
        "Prayer",
        "Religion, spirituality, and new age",
        "Textbook",
        "True crime",
        "Review",
        "Science",
        "Self help",
        "Sports and leisure",
        "Travel",
        "True crime",
    ],
}


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
        test_db.drop_all()
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


@pytest.fixture()
def book_genre():
    return random.choice(GENRE_DICT[random.choice(TOP_LEVEL_GENRE_CLASSIFICATION)])


@pytest.fixture()
def all_book_genre():
    fiction, non_fiction = GENRE_DICT.values()
    return fiction + non_fiction


def book_factory():
    while True:
        faker = Faker()
        fake_book_title = faker.text()
        book_genre = random.choice(
            GENRE_DICT[random.choice(TOP_LEVEL_GENRE_CLASSIFICATION)]
        )
        book = Book(title=fake_book_title, genre=book_genre)
        yield book


@pytest.fixture()
def new_book(db):
    book = next(book_factory())
    db.session.add(book)
    db.session.commit()
    return book


@pytest.fixture()
def books_more_than_quota(db, new_book):
    i = 0
    factory = book_factory()
    books = []
    while i < models.BORROWING_QUOTA + 1:
        book = next(factory)
        books.append(book)
        db.session.add(book)
        i += 1
    db.session.commit()
    return books


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
