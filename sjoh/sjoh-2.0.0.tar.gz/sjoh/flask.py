"""
Copyright (c) 2014, Nicolas Vanhoren

Released under the MIT license

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import unicode_literals, print_function, absolute_import

import sjoh
import flask
import logging
import traceback

_logger = logging.getLogger(__name__)

class SjohFlask(object):
    def __init__(self, app):
        self.app = app
        self.json_serializer = sjoh.JsonSerializer()

    def add_url_rule_for_json(self, rule, endpoint=None, view_func=None, *args, **kwargs):
        def nfunc():
            try:
                content = flask.request.get_json()
                arguments = self.json_serializer.from_json_types(content)
                assert isinstance(arguments, list), "Expected list: %s" % arguments
                error = False
                if view_func:
                    ret = view_func(*arguments)
                else:
                    ret = None
            except Exception as e:
                _logger.exception("Exception during request")
                nex = sjoh.to_json_exception(e)
                if self.app.config.get("SJOH_DEBUG", True):
                    nex.traceback = traceback.format_exc()
                error = True
                ret = nex
            resp = flask.make_response(self.json_serializer.stringify(ret), 500 if error else 200)
            resp.mimetype = "application/json"
            return resp
        if view_func:
            nfunc.__name__ = view_func.__name__
            nfunc.__module__ = view_func.__module__
        return self.app.add_url_rule(rule, endpoint, nfunc, *args, methods=["POST"], **kwargs)

    def json(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule_for_json(rule, endpoint, f, **options)
            return f
        return decorator
