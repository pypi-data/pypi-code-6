# -*- coding: utf-8 -*-

"""
decorators for textshaper
"""

string = (str, unicode)

class lines(object):
    """
    allow functions that process lists of lines of text to
    accept strings, lists of lines, or a file-like object
    """

    def __init__(self, function, line_separator='\n'):
        self.function = function
        self.line_separator = line_separator

        # record function information from function object
        self.func_name = function.func_name

    def __call__(self, text, *args, **kwargs):
        is_string = False
        if isinstance(text, string):
            is_string = True
            text = text.splitlines()
        retval = self.function(text, *args, **kwargs)
        if is_string:
            return self.line_separator.join(retval)
        return retval
