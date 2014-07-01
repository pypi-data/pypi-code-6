#!/usr/bin/python
# -*- coding: utf-8 -*-


def colors(color):
    '''Print colors'''

    paint = {
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'magenta': '\x1b[35m',
        'cyan': '\x1b[36m',
        'default': '\x1b[0m'
    }

    return paint[color]
