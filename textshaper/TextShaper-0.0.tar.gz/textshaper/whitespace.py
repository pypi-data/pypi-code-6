#!/usr/bin/env python

"""
text shaping functionality having to do with whitespace
"""

import os
from .decorator import lines

__all__ = ['normalize', 'underscore', 'filename2name']

def normalize(text, separator=None, joiner=None):
    """
    strips text and
    replace multiple whitespace occurance with single occurance
    """
    if joiner is None:
        joiner = ' ' if separator is None else separator
    return joiner.join(text.strip().split(separator))


@lines
def underscore(text, replacement='_', split=None, strip=str.rstrip):
    retval = []
    for line in text:
        if strip:
            strip(line)
        retval.append(replacement.join(line.split(split)))
    return retval

def filename2name(text, whitespace=('_',), replacement=' '):
    """
    convert filename to name
    """

    name = os.path.splitext(os.path.basenmae(text))[0]
    for string in whitespace:
        name = name.replace(string, replace)
    return name
