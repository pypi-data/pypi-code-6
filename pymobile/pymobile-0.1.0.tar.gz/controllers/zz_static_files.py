#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
import os

try:
    import pymobile
    root_path = os.path.join( os.path.split(pymobile.__file__)[0] or '.', 'static' )
except ImportError:
    root_path = os.path.join('.', 'static' )

# Statiske filer:
@bottle.route('/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=root_path)
