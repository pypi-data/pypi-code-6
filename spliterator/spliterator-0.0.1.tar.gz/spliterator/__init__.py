#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
spliterator
============

Split line streams into managable chunks

"""

from __future__ import print_function

import re

__author__ = 'Shane R. Spencer'
__author_email__ = "shane@bogomip.com"
__license__ = 'MIT'
__copyright__ = '2014 Shane R. Spencer'
__version__ = '0.0.1'
__status__ = "Prototype"
__url__ = "https://github.com/whardier/spliterator"
__description__ = "Split line streams into managable chunks"

START_EVENT = 'START'
END_EVENT = 'END'
LINE_EVENT = 'LINE'

BLANK_RE = re.compile('')

BLANK_LINE_RE = re.compile('^$')
BLANK_LINE_WITH_NEWLINES_RE = re.compile('^\s+?$')

def chunk(readable, matchable, newlines=False, autostart=False):

    started = False

    match_function = None

    if autostart:
        yield START_EVENT, None
        started = True
    if type(matchable) == type(BLANK_RE):
        match_function = matchable.match
    for line in readable:
        if not newlines:
            line = line.rstrip('\n').rstrip('\r')
        if not match_function and matchable in line:
            if started:
                yield END_EVENT, None
            yield START_EVENT, None
            started = True
        elif match_function and match_function(line):
            if started:
                yield END_EVENT, None
            yield START_EVENT, None
            started = True
        yield LINE_EVENT, line.rstrip()
    else:
        if started:
            yield END_EVENT, None

if __name__ == '__main__':
    for event, data in chunk(open('/etc/hosts'), BLANK_LINE_RE, autostart=True):
        print([event, data])

