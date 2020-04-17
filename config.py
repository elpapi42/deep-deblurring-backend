#!/usr/bin/python
# coding=utf-8

"""Default Config for production."""

import os

DEBUG = False
TESTING = False

SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
