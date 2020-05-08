#!/usr/bin/python
# coding=utf-8

"""This table stores a pair example of proceced images."""

import uuid
from datetime import datetime
import pytz

from sqlalchemy.dialects.postgresql import UUID, JSON

from deblurrer import db

class Example(db.Model):
    """
    Store the record of a consumed Example.

    The images fields are json encoded
    containing metada and resource location information
    """
    __tablename__ = "examples"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    input_image = db.Column(db.String, nullable=False)
    output_image = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.utc), nullable=False)

    def __init__(self, id, input_image, output_image):
        self.id = id
        self.input_image = input_image
        self.output_image = output_image

    def __repr__(self):
        return "<ID: {} Created: {}>".format(self.id, self.created)
