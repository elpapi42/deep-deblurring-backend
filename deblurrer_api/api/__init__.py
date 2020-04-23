#!/usr/bin/python
# coding=utf-8

"""API package."""

from flask import Blueprint

api_bp = Blueprint('api_bp', __name__)

from deblurrer_api.api import routes
