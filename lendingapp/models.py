import datetime

from lendingapp.db import db

BORROWING_QUOTA = 3
DEFAULT_LENDING_PERIOD = 21


class CheckoutException(Exception):
    pass


class QuotaException(CheckoutException):
    pass


class AlreadyBorrowedException(CheckoutException):
    pass


class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    borrowed_at = db.Column(db.Date, default=datetime.date.today())
    due_at = db.Column(
        db.Date,
        default=datetime.date.today() + datetime.timedelta(days=DEFAULT_LENDING_PERIOD),
    )
    book = db.relationship("Book", backref="borrower_checkouts")
    user = db.relationship("User", backref="borrowed_books_checkouts")
    db.UniqueConstraint("user_id", "book_id")

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "due_at": str(self.due_at),
            "borrowed_at": str(self.borrowed_at),
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    borrowing_limit = db.Column(db.Integer, default=BORROWING_QUOTA)
    borrowed_books = db.relationship("Book", secondary="checkout")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    genre = db.Column(db.Text)
    borrower = db.relationship("User", uselist=False, secondary="checkout")

    def to_json(self):
        return {"id": self.id, "title": self.title, "genre": self.genre}


def checkout(user, book):
    if len(user.borrowed_books) == user.borrowing_limit:
        raise QuotaException(
            f"user:{user} has reached borrowing limit of: {user.borrowing_limit}"
        )
    if book.borrower is not None:
        # though we have unique contraint lets check the condiniton here
        user_str = "you" if book.borrower == user else "another user"
        raise AlreadyBorrowedException(
            f"book: {book.title} has already been borrowed by {user_str}"
        )
    checkout = Checkout(user=user, book=book)
    db.session.add(checkout)
    db.session.commit()
    return checkout
