#!/usr/bin/python
# coding=utf-8

"""Logic for inference controller."""

from io import BytesIO
import requests
import base64

import numpy as np
from PIL import Image
from flask import make_response, request, jsonify
from flask import current_app as app
from flask_restful import Resource

from deblurrer_api.api.schemas import InferenceSchema
from marshmallow import ValidationError


class InferenceController(Resource):
    """Call the serving API for inference over the supplied image."""

    def post(self):
        """
        Send image to inference API.

        Returns:
            json response with the result of inference
        """
        input_schema = InferenceSchema()

        # Validates request json body
        try:
            input_data = input_schema.load(request.json)
        except ValidationError as err:
            return make_response(
                jsonify(err.messages),
                400,
            )

        # Decodes image as list
        image = input_data.get('image')
        image = Image.open(BytesIO(base64.b64decode(image)))
        image = np.asarray(image)
        image = np.stack([image], axis=0)
        image = image.tolist()

        output = requests.post(
            url=app.config['SERVING_URL'],
            json={'instances': image},
        ).json()

        return make_response(
            output,
            200,
        )
