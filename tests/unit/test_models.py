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
