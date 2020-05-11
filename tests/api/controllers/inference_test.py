#!/usr/bin/python
# coding=utf-8

"""Test the inference endpoint."""

import requests

from tests.conftest import patch_inference_request


def test_inference(client, image, monkeypatch):
    # Patch the external requests
    patch_inference_request(image, monkeypatch)

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