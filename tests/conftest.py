#!/usr/bin/python
# coding=utf-8

"""Stores fixtures used across all the tests."""


import os
import pytest
import requests
import pathlib
from io import FileIO
from base64 import urlsafe_b64encode

import cloudinary

from deblurrer import create_app, db, limiter

@pytest.fixture
def client():
    """Creates an http client and server for make requests."""
    app = create_app(config='flask_config.Testing')

    with app.app_context():
        limiter.enabled = False
        db.drop_all()
        db.create_all()

    return app.test_client()


@pytest.fixture
def image():
    """Loads and returns test image."""
    image_path = pathlib.Path(os.path.dirname(__file__))/'resources'/'test_image.jpg'
    return FileIO(str(image_path))

@pytest.fixture
def testfile():
    """Loads and returns test file."""
    file_path = pathlib.Path(os.path.dirname(__file__))/'resources'/'test_file.txt'
    return FileIO(str(file_path))

def patch_inference_request(image, monkeypatch):
    """
    Patch the external requests of inference endpoint.

    Reduce boilerplate when writing test that require
    the creation of an image pair example
    """
    # Bytes from test image for mock the inference engine response
    image_bytes = image.read()
    image.seek(0)

    # Mock inference engine response
    class MockResponse(object):
        def __init__(self):
            self.status_code = 200

        def json(self):
            return {
                'predictions': [urlsafe_b64encode(image_bytes)],
            }

    def mock_post(url, json):
        return MockResponse()
    
    # Path post function
    monkeypatch.setattr(requests, 'post', mock_post)

    # Mock cloudinary responses
    def mock_upload(file, public_id, folder):
        return {
            'secure_url': 'https://res.cloudinary.com/test.jpg'
        }

    # Path upload method
    monkeypatch.setattr(cloudinary.uploader, 'upload', mock_upload)