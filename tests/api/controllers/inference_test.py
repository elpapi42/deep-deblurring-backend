#!/usr/bin/python
# coding=utf-8

"""Test the inference endpoint."""

def test_inference(client):
    data = dict(
        file=(BytesIO(b'my file contents'), "work_order.123"),
    )

    assert data != data
