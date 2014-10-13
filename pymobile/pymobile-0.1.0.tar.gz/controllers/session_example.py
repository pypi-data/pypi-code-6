#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from pymobile import shared
import settings

# Eksempel på login-greier
@bottle.get('/session')
@bottle.view('session')
def login_form():
    return dict(session=shared.session)

@bottle.post('/session') # or @route('/login', method='POST')
@bottle.view('session')
def login_submit():
    shared.session['test1'] = bottle.request.forms.get('test1')
    shared.session['test2'] = bottle.request.forms.get('test2')
    shared.session['test3'] = bottle.request.forms.get('test3')
    shared.session['test4'] = bottle.request.forms.get('test4')
    return dict(session=shared.session)
