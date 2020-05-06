#!/usr/bin/python
# coding=utf-8

"""Initialize application."""


import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

cors = CORS()
marsh = Marshmallow()
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
    limiter.init_app(app)

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix='/api')

        """
        # Drop all the tables from test database if in test mode
        if (app.testing):
            db.drop_all()

        # Create table for models
        db.create_all()
        """

        return app
