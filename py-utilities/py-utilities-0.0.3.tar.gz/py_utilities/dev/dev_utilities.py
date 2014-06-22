#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import functools
import warnings
import webbrowser


def browser(html, ip='127.0.0.1', port=0):  # pragma: no cover
    class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):
            self.wfile.write(html)

    server = BaseHTTPServer.HTTPServer((ip, port), RequestHandler)
    webbrowser.open("http://{0}:{1}".format(*server.server_address))
    server.handle_request()


def deprecated(message=""):
    def decorator(deprecated_func):
        msg = message or \
            "Function '{0}' is deprecated.".format(deprecated_func.__name__)

        @functools.wraps(deprecated_func)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return deprecated_func(*args, **kwargs)
        return wrapper
    return decorator

# vim: filetype=python
