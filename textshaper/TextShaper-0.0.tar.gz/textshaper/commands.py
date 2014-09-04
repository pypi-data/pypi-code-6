# -*- coding: utf-8 -*-

"""
CLI commands for textshaper
"""

import inspect

class Shaper(object):
    """
    individual text shaper component
    (function wrapper)
    """

    def __init__(self, function):
        self.function = function
        self.func_name = function.func_name

    def __call__(self, text, **kwargs):
        return self.function(text, **kwargs)

    def __str__(self):
        return self.func_name


class Commands(object):

    def __init__(self):
        self.shapers = []
        self.keys = {}
        self.display_keys = []

    def add(self, function, key=None):
        self.shapers.append(Shaper(function))
        if not key:
            key = str(self.shapers[-1])
        key = key.lower()
        self.keys[key] = self.shapers[-1]
        name = str(self.shapers[-1]).lower()
        if name.startswith(key):
            display_name = '{}{}'.format(key, name[len(key):].upper())
        else:
            display_name = '{}:{}'.format(key, name.upper())
        self.display_keys.append(display_name)

    def call(self, key, text, **kwargs):
        if key in self.keys:
            return self.keys[key](text, **kwargs)

    __call__ = call

    def display(self):
        return ' '.join(self.display_keys)
