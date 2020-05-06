#!/usr/bin/python
# coding=utf-8

"""Gunicorn server config."""

import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count()
