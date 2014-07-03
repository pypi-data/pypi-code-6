# coding: utf-8
'''
File: scope.py
Author: Oliver Zscheyge
Description:
    -
'''

class Scope(object):
    """Scope and category types.
    E.g. used to organize heuristics, features/metrics or rules.
    """
    UNSPECIFIED = 0

    DOCUMENT  = 1 << 0
    SECTION   = 1 << 1
    CHAPTER   = 1 << 2
    PAGE      = 1 << 3
    PAGES     = 1 << 4
    PARAGRAPH = 1 << 5
    SENTENCE  = 1 << 6
    WORD      = 1 << 7
    FLOAT     = 1 << 8

    LANGUAGE  = 1 << 16
    FORM      = 1 << 17
    CONTENT   = 1 << 18

