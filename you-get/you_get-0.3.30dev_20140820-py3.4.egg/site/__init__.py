#!/usr/bin/env python

from importlib import import_module
import os

_filepath = os.path.dirname(os.path.realpath(__file__))
names = [ i[:-3] for i in os.listdir(_filepath)
            if os.path.isfile(os.path.join(_filepath, i))
                and i[-3:] == '.py'
                and i[0] != '_' ]
extractors = [ import_module('{}.{}'.format(__name__, i)).extractor for i in names ]
