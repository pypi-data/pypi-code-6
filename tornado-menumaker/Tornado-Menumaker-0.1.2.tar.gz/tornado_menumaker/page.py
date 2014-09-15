#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
import inspect
from tornado.web import Application

from .route import Route
from .index import IndexRoute

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 23:46'


class Page(Route):
    """
        A Page
    """

    def __init__(self, url: str=None, **kwargs):
        super().__init__(url=url, **kwargs)

        self._index = None

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], Application):
            if self._index is not None:
                return self._index(*args, **kwargs)

            self.handler = self.cls(*args, **kwargs)
            self.handler.reverse_url_name = self.name
            return self.handler
        elif isinstance(args[0], type):
            self.cls = args[0]

            for n, route in inspect.getmembers(self.cls, Route.isroute):
                route.url = self._url.rstrip('/') + '/' + route.url.lstrip('/')
                route.cls = self.cls

            for n, method in inspect.getmembers(self.cls, IndexRoute.isindex):
                self._index = method

            return self.cls
        raise TypeError("%s is not decorating a class, "
                        "use @subpage for decorating a method" % (len(args[0]) and type(args[0]) or "@page"))
