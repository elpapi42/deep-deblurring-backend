#!/usr/bin/python
# coding=utf-8

"""Logic for inference controller."""

from flask import make_response, request, jsonify
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

        # Deserialize and validates request json body
        try:
            input_data = input_schema.load(request.json)
        except ValidationError as err:
            return make_response(
                jsonify(err.messages),
                400,
            )

        return make_response(
            jsonify(input_data),
            200,
        )
