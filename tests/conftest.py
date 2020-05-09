#!/usr/bin/python
# coding=utf-8

"""Stores fixtures used across all the tests."""


import os
import pytest
import requests

from deblurrer import create_app, db

@pytest.fixture
def client():
    """Creates an http client and server for make requests."""
    app = create_app(config='flask_config.Testing')

    # Setup teesting config
    app.debug = True
    app.testing = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'TESTING_DATABASE_URI',
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app.test_client()
    