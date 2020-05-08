#!/usr/bin/python
# coding=utf-8

"""API routes definition."""


from flask_restful import Api

from deblurrer.api import api_bp
from deblurrer.api.controllers import InferenceController

api = Api(api_bp)

api.add_resource(InferenceController, '/inference/')
