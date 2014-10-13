#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from pymobile import shared

# startside

@bottle.route('/')
@bottle.view('index')
def index(name='World'):
    return dict(livecounter=shared.state['livecounter'])

