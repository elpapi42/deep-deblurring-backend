#!/usr/bin/python
# coding=utf-8

"""Stores fixtures used across all the tests."""


import os
import pytest
import requests
import pathlib
from io import FileIO

from deblurrer import create_app, db

@pytest.fixture
def client():
    """Creates an http client and server for make requests."""
    app = create_app(config='flask_config.Testing')

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app.test_client()


@pytest.fixture
def image():
    """Loads and returns test image."""
    image_path = pathlib.Path(os.path.dirname(__file__))/'resources'/'test_image.jpg'
    return FileIO(str(image_path))