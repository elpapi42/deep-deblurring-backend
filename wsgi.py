#!/usr/bin/python
# coding=utf-8

"""wsgi server for local testing."""

from deblurrer import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
