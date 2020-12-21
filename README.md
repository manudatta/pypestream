## Overview

This Flask application contains the basic book lending app 

## Motivation and Approach

Assignment

- Started with unit tests and schema design
- After writing the code for passing unit tests moved on to api and working on functional test
- The tests cover bare minimum api as part of assigment
- No tests to check proper error conditions

## How to Run

In the top-level directory:

    $ export FLASK_APP=lendingapp
    $ export FLASK_ENV=development
    $ flask run

## Installation Instructions

Pull down the source code from this GitLab repository:

```sh
git clone https://github.com/manudatta/pypestream.git```

Create a new virtual environment:

```sh
$ cd pypestream 
$ python3 -m venv venv
```

Activate the virtual environment:

```sh
$ source venv/bin/activate
```

Install the python packages in requirements.txt:

```sh
(venv) $ pip install -r requirements.txt
```

Set the module that contains the Flask application and specify that the development environment should be used:

```sh
(venv) $ export FLASK_APP=lendingapp
(venv) $ export FLASK_ENV=development
```

Run development server to serve the Flask application:

```sh
(venv) $ flask run
```

## Key Python Modules Used

- Flask: micro-framework for web application development
- SQLAlchemy - ORM (Object Relational Mapper)
- Flask-Restful - simplifies rest

This application is written using Python 3.8.6.

## Testing

```sh
(venv) $ python -m pytest
```