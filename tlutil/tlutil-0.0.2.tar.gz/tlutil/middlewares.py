# -*- coding: utf-8 -*-
"""
    tlutil.middlewares
"""


__all__ = [
    "RealIPFix"
]


class RealIPFix(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        real_ip = environ.get('HTTP_X_REAL_IP')
        if real_ip:
            environ['REMOTE_ADDR'] = real_ip
        return self.app(environ, start_response)
