#!/usr/bin/python
# coding=utf-8

"""Status of the server and parametric variables."""

from flask import make_response, jsonify, current_app as app
from flask_restful import Resource, abort

from deblurrer import limiter


class StatusController(Resource):
    """
    Make avaiable high level information about the api status.

    Things like max accepted image size or resolution
    Can be used for consult the status of the api asdumy request
    """

    decorators = [limiter.limit('1/second', methods=['GET'])]

    def get(self):
        return make_response(
            jsonify({
                'max_image_size': app.config.get('MAX_CONTENT_LENGTH'),
                'max_image_res': app.config.get('MAX_IMAGE_RESOLUTION'),
            }),
            200,
        )