#!/usr/bin/python
# coding=utf-8

"""Logic for inference controller."""

from io import BytesIO
import requests
import base64

from PIL import Image, UnidentifiedImageError
from flask import make_response, request, jsonify
from flask import current_app as app
from flask_restful import Resource, abort

from deblurrer_api.api.schemas import ImageSchema
from marshmallow import ValidationError


class InferenceController(Resource):
    """Call the serving API for inference over the supplied image."""

    def post(self):
        """
        Send image to inference API.

        Returns:
            json response with the result of inference
        """
        image_schema = ImageSchema()

        # Validates request json body
        try:
            input_data = image_schema.load(request.json)
            b64image = input_data.get('image')
            # Tries open image, aviod injection of other type of files
            Image.open(BytesIO(base64.b64decode(b64image)))
        except ValidationError as err:
            abort(
                400,
                message='Received invalid JSON',
                payload=err.messages,
            )
        except UnidentifiedImageError:
            abort(
                400,
                message='File cant be identified as image',
            )

        # Request predictions to inference engine
        output = requests.post(
            url=app.config['SERVING_URL'],
            json={'instances': [
                [{'b64': r'{string}'.format(string=b64image)}],
            ]},
        ).json()

        # Validates inference engine reponse
        if (output.get('error') is not None):
            abort(
                500,
                message='Inference engaine error',
                payload=output['error'],
            )

        # Base64URL to Base64
        output_image = output['predictions'][0]
        output_image = output_image.replace('-', '+')
        output_image = output_image.replace('_', '/')

        return make_response(
            jsonify({'image': output_image}),
            200,
        )
