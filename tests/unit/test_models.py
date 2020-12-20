"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from faker import Faker
from lendingapp.models import User


def test_new_user(db):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, borrowing_limit and borrowed_books fields are defined correctly
    """
    faker = Faker()
    fake_name = faker.name()
    user = User(name=fake_name)
    db.session.add(user)
    db.session.flush()
    assert user.name == fake_name, "user name matches"
    assert user.borrowing_limit == 3, "default borrowing limit for user is correct"
    assert user.id is not None, "user id is populated"


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created via fixture
    THEN check the name, borrowing_limit and borrowed_books fields are defined correctly
    """
    assert new_user.borrowing_limit == 3, "default borrowing limit for user is correct"
    assert new_user.id is not None, "user id is populated"


def test_new_book_with_fixture(new_book, all_book_genre):
    """
    GIVEN a Book model
    WHEN a new Book is created via fixture
    THEN check the id, title, and genre fields are defined correctly
    """
    assert new_book.id is not None, "book id is populated"
    assert len(new_book.title) > 1, "book title is not 0 length"
    assert new_book.genre in all_book_genre
