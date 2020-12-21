"""
This file (test_apis.py) contains the functional tests for the lending app

These tests use various verbs to different URLs to check for the proper behavior
of the api
"""
import pytest

from lendingapp.models import checkout, Book


def test_user_borrowed_books(client,new_user,books_more_than_quota):
    user_id = new_user.id
    endpoint = f'/api/users/{user_id}/books'
    response = client.get(endpoint)
    assert response.status_code == 200
    result = response.json
    assert 'borrowed_books' in result, "key borrowed_books is present in results"
    assert result['borrowed_books'] == [], "no books have been borrowed so far"
    book_count = 2
    for book in books_more_than_quota[0:book_count]:
        checkout(user=new_user,book=book)
    response = client.get(endpoint)
    assert response.status_code == 200
    result = response.json
    assert 'borrowed_books' in result, "key borrowed_books is present in results"
    assert len(result['borrowed_books']) == book_count , "books have been borrowed so far has right count"
    assert result['borrowed_books'] == [book.to_json() for book in books_more_than_quota[0:book_count]] , "book borrowed match the records"


def test_due_books(client,new_user,second_user,books_more_than_quota):
    endpoint = f'/api/books?is_due=1'
    for book in books_more_than_quota[0:2]:
        checkout(user=new_user,book=book)
    checkout(user=second_user, book=books_more_than_quota[-2])
    response = client.get(endpoint)
    result = response.json
    assert response.status_code == 200
    assert 'books' in result, "key books is present in results"
    assert len(result['books']) == 3 , "correct number of books is returned"
    json_book_list = [book.to_json() for book in books_more_than_quota[0:3]]
    for book in json_book_list:
        assert book in result['books'], "book borrowed match the records"

def test_create_checkout(client,new_user,new_book):
    endpoint = f'/api/checkouts'
    data = {'user_id':new_user.id, 'book_id': new_book.id}
    response = client.post(endpoint,data=data)
    result = response.json
    assert response.status_code == 200
    assert 'checkout' in result, "key checkout is present in results"
    checkout = result['checkout']
    assert checkout['user_id'] == new_user.id , "user is correct"
    assert checkout['book_id'] == new_book.id, "book is correct"

def test_delete_book(client,new_book):
    book_id = new_book.id
    endpoint = f'/api/book/{book_id}'
    assert len(Book.query.all()) == 1, "assert only one book is in db"
    response = client.delete(endpoint)
    assert response.status_code == 200
    result = response.json
    assert response.status_code == 200
    assert 'book' in result, "key book is present in results"
    book = result['book']
    assert book['id'] == new_book.id, "correct book is deleted"
