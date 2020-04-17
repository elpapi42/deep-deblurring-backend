#!/usr/bin/python
# coding=utf-8

"""API routes definition."""


from flask_restful import Api

from . import api_bp
from .controllers import HomeController

api = Api(api_bp)

api.add_resource(HomeController, '/home/')
