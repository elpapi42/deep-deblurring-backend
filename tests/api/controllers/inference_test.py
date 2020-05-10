#!/usr/bin/python
# coding=utf-8

"""Test the inference endpoint."""

import requests
from base64 import urlsafe_b64encode

import cloudinary


def test_inference(client, image, monkeypatch):
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

    # Make the request to the api
    file = {'image': image}
    response = client.post(
        'api/inference/',
        content_type='multipart/form-data',
        data=file,
    ).json

    assert response == {
        'input_image': 'https://res.cloudinary.com/test.jpg',
        'output_image': 'https://res.cloudinary.com/test.jpg',
        'resource_id': response.get('resource_id'),
    }

def test_inference_when_engine_unavailable(client, image, monkeypatch):
    def mock_post(url, json):
        raise requests.exceptions.ConnectionError()
    
    # Patch post function
    monkeypatch.setattr(requests, 'post', mock_post)
    
    # Make the request to the api
    file = {'image': image}
    response = client.post(
        'api/inference/',
        content_type='multipart/form-data',
        data=file,
    ).json

    assert response == {
        'message': 'Inference engine unavailable',
    }

def test_inference_against_invalid_file(client, testfile):
    # Make the request to the api
    file = {'image': testfile}
    response = client.post(
        'api/inference/',
        content_type='multipart/form-data',
        data=file,
    ).json

    assert response == {'message': 'Invalid file'}