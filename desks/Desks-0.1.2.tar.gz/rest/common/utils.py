#!/usr/bin/env python

from flask import current_app
from shelves import shelves

def get_shelf():
    """
    This helps to get a shelf
    """
    shelf = getattr(current_app, 'shelf', None)
    if shelf is None:
        raise Exception('Oops, no shelf')

    return shelf
