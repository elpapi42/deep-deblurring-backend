#!/usr/bin/python
# coding=utf-8

"""Initialize application."""


import os
from os.path import join, dirname

import cloudinary
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

cors = CORS()
marsh = Marshmallow()
db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['5/minute', '1/second'],
)

from deblurrer_api.api import api_bp


def create_app(testing=False):
    """
    Init core application.

    Args:
        testing (bool): if true, the app will be ready for be tested

    Returns:
        Application instance
    """
    # Load .env vars
    dotenv_path = join(dirname(dirname(__file__)), '.env')
    load_dotenv(dotenv_path)

    # Setup default production config
    app = Flask('deblurrer', instance_relative_config=True)
    app.config.from_object('flask_config')

    # Init Cloudinary credentials
    cloudinary.config(
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key = os.environ.get('CLOUDINARY_API_KEY'),
        api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    )

    # Enable testing features when unit testing
    if (testing):
        app.debug = True
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'TESTING_DATABASE_URI',
        )

    # Init Plugins
    cors.init_app(app)
    marsh.init_app(app)
    db.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix='/api')

        # Drop all the tables from test database if in test mode
        if (app.testing):
            db.drop_all()

        # Create table for models
        db.create_all()

        return app
