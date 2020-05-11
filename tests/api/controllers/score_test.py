#!/usr/bin/python
# coding=utf-8

"""Test the score endpoint."""

import uuid

from tests.conftest import patch_inference_request


def test_score(client, image, monkeypatch):
    # Patch the external requests
    patch_inference_request(image, monkeypatch)

    # Create new entry in database
    file = {'image': image}
    response = client.post(
        'api/inference/',
        content_type='multipart/form-data',
        data=file,
    ).json
    
    # Assign score to the recently created example
    data = {
        'resource_id': response.get('resource_id'),
        'score': 4,
    }
    response = client.put(
        'api/score/',
        json=data,
    )

    assert response.status_code == 200

def test_bad_score(client, image, monkeypatch):
    # Patch the external requests
    patch_inference_request(image, monkeypatch)

    # Create new entry in database
    file = {'image': image}
    response = client.post(
        'api/inference/',
        content_type='multipart/form-data',
        data=file,
    ).json
    
    # Assign score to the recently created example
    data = {
        'resource_id': response.get('resource_id'),
        'score': 8,
    }
    response = client.put(
        'api/score/',
        json=data,
    ).json

    assert response == {
        'message': 'Invalid request body arguments',
        'payload': "{'score': ['Must be greater than or equal to 0 and less than or equal to 5.']}",
    }

def test_resource_not_found(client, image, monkeypatch):
    # Patch the external requests
    patch_inference_request(image, monkeypatch)

    # Create new entry in database
    file = {'image': image}
    response = client.post(
        'api/inference/',
        content_type='multipart/form-data',
        data=file,
    ).json
    
    # Assign score to the recently created example
    data = {
        'resource_id': 'f45d6ced-29d8-49e1-a4ba-404792548cba',
        'score': 3,
    }
    response = client.put(
        'api/score/',
        json=data,
    ).json

    assert response == {'message': 'Not found'}