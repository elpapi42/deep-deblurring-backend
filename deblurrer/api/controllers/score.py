#!/usr/bin/python
# coding=utf-8

"""Logic for score asignament controller."""

from flask import make_response, request, jsonify
from flask import current_app as app
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from deblurrer.api.schemas import ScoreSchema
from deblurrer.api.models import Example
from deblurrer import db


class ScoreController(Resource):
    """Assign a user subjective score to a resource in db."""

    def put(self):
        """
        Update the subjective score.

        The images must be already on the database
        and uploaded to cloudinary

        Returns:
            Ok
        """
        score_schema = ScoreSchema()
        errors = score_schema.validate(request.json)
        if (errors):
            abort(
                400,
                message='Invalid request body arguments',
                payload=str(errors),
            )

        example = Example.query.get(request.json.get('resource_id'))
        if (example is None):
            abort(404, message='Not found')

        example.score = request.json.get('score')
        db.session.add(example)
        db.session.commit()

        return make_response()