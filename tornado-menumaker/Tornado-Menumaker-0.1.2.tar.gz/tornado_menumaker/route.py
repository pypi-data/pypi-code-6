#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
from functools import partial
import inspect
import re
from types import FunctionType
from tornado.web import URLSpec, Application, RequestHandler

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 23:48'

SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS


class Route(URLSpec):
    """
        Represent a route
    """

    def __init__(self, url: str=None, **kwargs):
        super().__init__(url, self, kwargs=kwargs)

        self._url = url
        self._routing = {}

    @property
    def url(self):
        """
            URL of Route (plain without modification)
        """
        return self._url

    @url.setter
    def url(self, pattern: str):
        """
            Set a new url as pattern

            :param pattern: New url value
        """
        self._url = pattern
        if not pattern.endswith('$'):
            pattern += '$'
        self.regex = re.compile(pattern)
        assert len(self.regex.groupindex) in (0, self.regex.groups), \
            ("groups in url regexes must either be all named or all "
             "positional: %r" % self.regex.pattern)
        self._path, self._group_count = self._find_groups()

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            if item.upper() in SUPPORTED_METHODS:
                return partial(self.register, method=item.lower())

    def register(self, function: FunctionType, method: str):
        """
            Register a method function

            :param function: Function to be registered
            :param method: Name of method
        """
        self._routing[method] = function
        return self

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return self._routing['get'].__get__(instance, cls)

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], FunctionType):
            self._routing['get'] = args[0]
            self.__module__ = inspect.getmodule(args[0])
            self.__clsname__ = args[0].__qualname__.rsplit(".", 3)[-2]
            self.name = "%s.%s" % (self.__module__, args[0].__qualname__)
            return self
        elif isinstance(args[0], Application):
            try:
                self.handler = self.cls(*args, **kwargs)
            except AttributeError:
                self.cls = getattr(self.__module__, self.__clsname__)
                self.handler = self.cls(*args, **kwargs)
            for method, function in self._routing.items():
                setattr(self.handler, method, function.__get__(self.handler))
            self.handler.route = self
            return self.handler
        raise Exception()

    def __repr__(self):
        return '%s(%s, kwargs=%r, name=%r)' % \
               (self.__class__.__name__, self.url, self.kwargs, self.name)

    @classmethod
    def isroute(cls, other: object) -> bool:
        """
            Is other an instance of Route?

            :param other: Object to compare
        """
        return isinstance(other, cls)

