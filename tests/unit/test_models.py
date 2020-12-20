"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
import datetime

import pytest
from faker import Faker

import lendingapp
from lendingapp.models import User, Checkout


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


def test_new_checkout(db, new_user, new_book):
    """
    GIVEN a Book model and User model
    WHEN a new Checkout is created
    THEN check the user.borrowed_books, book.borrower fields are defined correctly
    """
    checkout = Checkout(book=new_book, user=new_user)
    db.session.add(checkout)
    db.session.flush()
    today = datetime.date.today()
    borrowed_books = new_user.borrowed_books
    borrower = new_book.borrower
    assert len(borrowed_books) == 1, "user has borrowed one book"
    assert borrower == new_user, "new_user is the borrower"
    assert checkout.id is not None, "checkout id is populated"
    assert checkout.borrowed_at == today, "it is borrowed today"
    assert checkout.due_at == today + datetime.timedelta(
        days=lendingapp.models.DEFAULT_LENDING_PERIOD
    ), "it is due at correct day"


def test_checkout_limit(new_user, books_more_than_quota):
    """
    GIVEN a user and books
    WHEN a new Checkout is created for a books where quota exceeds
    THEN QuotaException is thrown
    """
    for i in range(lendingapp.models.BORROWING_QUOTA):
        book = books_more_than_quota[i]
        checkout = lendingapp.models.checkout(user=new_user, book=book)
        today = datetime.date.today()
        borrowed_books = new_user.borrowed_books
        borrower = book.borrower
        assert len(borrowed_books) == i + 1, "user has borrowed one book"
        assert borrower == new_user, "new_user is the borrower"
        assert checkout.id is not None, "checkout id is populated"
        assert checkout.borrowed_at == today, "it is borrowed today"
        assert checkout.due_at == today + datetime.timedelta(
            days=lendingapp.models.DEFAULT_LENDING_PERIOD
        ), "it is due at correct day"
    last_book = books_more_than_quota[-1]
    with pytest.raises(lendingapp.models.QuotaException):
        checkout = lendingapp.models.checkout(user=new_user, book=last_book)


def test_borrowing_same_book_again(new_user, new_book):
    """
    GIVEN a user and books
    WHEN a new Checkout is created for a book which is already borrowed
    THEN AlreadyBorrowedException is raised
    """
    checkout = lendingapp.models.checkout(user=new_user, book=new_book)
    with pytest.raises(lendingapp.models.AlreadyBorrowedException):
        checkout = lendingapp.models.checkout(user=new_user, book=new_book)


def test_returning_a_book(db, new_user, new_book):
    """
    GIVEN a user and books
    WHEN a checkout is deleted
    THEN borrower is set to None for the book and borrowed_books go down by 1
    """
    checkout = lendingapp.models.checkout(user=new_user, book=new_book)
    db.session.delete(checkout)
    db.session.commit()
    borrowed_books = new_user.borrowed_books
    borrower = new_book.borrower
    assert len(borrowed_books) == 0, "user has no borrowed books"
    assert borrower is None, "new_user is the borrower"
