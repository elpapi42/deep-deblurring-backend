#!/usr/bin/python
# coding=utf-8

"""Logic for inference controller."""

from requests.exceptions import ConnectionError
import requests
import base64
import imghdr
import uuid

from flask import make_response, request, jsonify
from flask import current_app as app
from flask_restful import Resource, abort
from cloudinary import uploader

from deblurrer.api.models import Example
from deblurrer import db


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
        input_image = request.files.get('image')
        if (input_image is None):
            abort(
                400,
                message='Image was not supplied'
            )
        
        # Checks if the file is an image
        input_image = input_image.read()
        if (not is_image(input_image)):
            abort(
                400,
                message='Invalid file'
            )

        image = str(base64.b64encode(input_image), encoding='utf-8')

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
        output_image = base64.urlsafe_b64decode(output_image)

        # Identifier of the images stored in cloudinary
        resource_id = uuid.uuid4()

        # Upload the input image
        input_resp = uploader.upload(
            bytearray(input_image),
            public_id=str(resource_id),
            folder='/input',
        )

        # Upload the generated image
        output_resp = uploader.upload(
            bytearray(output_image),
            public_id=str(resource_id),
            folder='/generated',
        )

        # Create and commit new example to append to the database
        example = Example(
            resource_id,
            input_resp.get('secure_url'),
            output_resp.get('secure_url'),
        )
        db.session.add(example)
        db.session.commit()

        return make_response(
            jsonify({
                'input_image': input_resp.get('secure_url'),
                'output_image': output_resp.get('secure_url'),
                'resource_id': str(resource_id),
            }),
            200,
        )
