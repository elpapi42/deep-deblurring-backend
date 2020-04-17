#!/usr/bin/python
# coding=utf-8

"""Logic for home controller."""

from flask import make_response, jsonify
from flask_restful import Resource


class HomeController(Resource):
    """Home endpoint."""

    def get(self, *args, **kwargs):
        return make_response(
            jsonify({'response': 'hello user'}),
            200,
        )
