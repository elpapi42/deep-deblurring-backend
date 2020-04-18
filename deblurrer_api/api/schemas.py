#!/usr/bin/python
# coding=utf-8

"""Marshmallow schemas for the API."""

from marshmallow import validate

from deblurrer_api import marsh


class InferenceSchema(marsh.Schema):
    """Defines and validates Base64 input image."""

    image = marsh.String(required=True, validate=validate.Length(1))
