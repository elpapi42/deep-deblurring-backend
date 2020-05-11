#!/usr/bin/python
# coding=utf-8

"""Marshmallow schemas for the API."""

from marshmallow.validate import Range

from deblurrer import marsh


class ScoreSchema(marsh.Schema):
    """Validates score assignament request json body."""

    resource_id = marsh.UUID(required=True)
    score = marsh.Integer(required=True, validate=Range(min=0, max=5))
