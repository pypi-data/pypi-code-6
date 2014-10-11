#!/usr/bin/python
# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import with_statement, print_function

from .js import minify
from .utils import json


def load(f):
    return loads(f.read())

def loads(source):
    try:
        minified = minify(source)
        return json.loads(minified)
    except json.JSONDecodeError as e:
        s = minified.split('\n')
        context = s[e.lineno-1][max(0, e.colno-1):e.colno+30]
        msg = e.msg + ' at ' + context
        raise json.JSONDecodeError(msg, minified, e.pos)
