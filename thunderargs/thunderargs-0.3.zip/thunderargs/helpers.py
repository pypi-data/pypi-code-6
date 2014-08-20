__author__ = 'thunder'

from functools import wraps as orig_wraps, WRAPPER_ASSIGNMENTS


WRAPPER_ASSIGNMENTS += ('__annotations__',)

wraps = lambda x: orig_wraps(x, WRAPPER_ASSIGNMENTS)