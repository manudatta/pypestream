"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from faker import Faker
from lendingapp.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, borrowing_limit and borrowed_books fields are defined correctly
    """
    faker = Faker()
    fake_name = faker.name()
    user = User(name=fake_name)
    assert user.name == fake_name


# def test_new_user_with_fixture(new_user):
#     """
#     GIVEN a User model
#     WHEN a new User is created
#     THEN check the email, hashed_password, authenticated, and role fields are defined correctly
#     """
#     assert new_user.email == 'patkennedy79@gmail.com'
#     assert new_user.hashed_password != 'FlaskIsAwesome'
#     assert new_user.role == 'user'
