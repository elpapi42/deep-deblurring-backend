#!/usr/bin/python
# coding=utf-8

"""Initialize application."""


import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from deblurrer_api.api import api_bp

cors = CORS()


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
    app = Flask('todolist', instance_relative_config=True)
    app.config.from_object('config')

    # Enable testing features when unit testing
    if (testing):
        app.debug = True
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'TESTING_DATABASE_URI',
        )

    # Init Plugins
    cors.init_app(app)

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
