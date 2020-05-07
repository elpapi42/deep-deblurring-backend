#!/usr/bin/python
# coding=utf-8

"""Logic for inference controller."""

from requests.exceptions import ConnectionError
import requests
import base64
import imghdr

from flask import make_response, request, jsonify
from flask import current_app as app
from flask_restful import Resource, abort


def is_image(file_bytes):
    """
    Check if the supplied bytes are from an image file.

    Args:
        file_bytes (bytes): Bytes of the file to check

    Returns:
        True if the file is validated as an image
    """
    return imghdr.what(file=None, h=file_bytes) in {'png', 'jpg', 'jpeg'}


class InferenceController(Resource):
    """Call the serving API for inference over the supplied image."""

    def post(self):
        """
        Send image to inference API.

        Returns:
            json response with the result of inference
        """
        image = request.files.get('image')
        if (image is None):
            abort(
                400,
                message='Image was not supplied'
            )
        
        # Checks if the file is an image
        image = image.read()
        if (not is_image(image)):
            abort(
                400,
                message='Invalid file'
            )

        image = str(base64.b64encode(image), encoding='utf-8')

        try:
            # Request predictions to inference engine
            preds = requests.post(
                url=app.config['SERVING_URL'],
                json={'instances': [
                    [{'b64': r'{string}'.format(string=image)}],
                ]},
            ).json()
        except ConnectionError:
            abort(
                500,
                message='Inference engine unavailable'
            )

        # Validates inference engine reponse
        if (preds.get('error') is not None):
            abort(
                500,
                message='Inference engine error',
            )

        # Base64URL to Base64
        output_image = preds['predictions'][0]
        output_image = output_image.replace('-', '+')
        output_image = output_image.replace('_', '/')

        return make_response(
            jsonify({'image': output_image}),
            200,
        )
