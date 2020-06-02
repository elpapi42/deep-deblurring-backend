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
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL')

    SERVING_URL = os.environ.get('SERVING_URL')

    # MAX_IMAGE_SIZE is on Megabytes
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_IMAGE_SIZE')) * 1024 * 1024
    MAX_IMAGE_RESOLUTION = int(os.environ.get('MAX_IMAGE_RESOLUTION'))

class Testing(Production):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI')
    RATELIMIT_STORAGE_URL = os.environ.get('TESTING_REDIS_URL')
