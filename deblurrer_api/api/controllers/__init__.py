#!/usr/bin/python
# coding=utf-8

"""Contains api controllers."""


from flask import make_response, jsonify


def format_response(message, status, message_type='message'):
    """
    Format error responses from the API.

    Useful for api responses uniformity, saves boilerplate writing controllers

    """
    return make_response(
        jsonify({message_type: message}),
        status,
    )


from .home import HomeController
