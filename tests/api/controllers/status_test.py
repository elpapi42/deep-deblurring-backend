#!/usr/bin/python
# coding=utf-8

"""Test the status endpoint."""


def test_status(client):
    response = client.get('api/')

    assert response.status_code == 200
    assert response.json == {
        'max_image_res': 1024,
        'max_image_size': 5242880,
    }