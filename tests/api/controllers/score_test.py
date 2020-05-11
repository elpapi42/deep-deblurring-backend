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