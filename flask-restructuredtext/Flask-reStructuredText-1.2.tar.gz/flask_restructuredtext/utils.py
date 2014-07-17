# -*- coding: utf-8 -*-

import re

from docutils.parsers.rst import directives
from flask import current_app

alignments = {
    'left': '0',
    'center': '0 auto',
    'right': '0 0 0 auto',
}


COLOR_PATTERN = re.compile("([a-f]|[A-F]|[0-9]){3}(([a-f]|[A-F]|[0-9]){3})")


def align(argument):
    """"""

    return directives.choice(argument, ('left', 'center', 'right'))


def get_ssl():
    """Check if SSL/TLS is forced.

    :type return: bool

    """
    return (current_app.config.get('FORCE_SSL', False) or
            current_app.config.get('FORCE_TLS', False))


def color(argument):
    match = COLOR_PATTERN.match(argument)
    if match:
        return argument
    else:
        raise ValueError('argument must be an hexadecimal color number')
