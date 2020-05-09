#!/usr/bin/python
# coding=utf-8

"""Default Config for production."""

import os


class Production(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    SERVING_URL = os.environ.get('SERVING_URL')

    MAX_CONTENT_LENGTH = 4 * 1024 * 1024

class Testing(Production):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI')
