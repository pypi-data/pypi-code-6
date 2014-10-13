#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from pymobile import shared
import settings

def check_user_credentials(u,p):
    #TODO replace with proper usercheck
    return (u == settings.username and p == settings.password)  #  :--) 


# Eksempel på login-greier


@bottle.get('/login')
def login_form():
    if shared.session['user']:
        return bottle.template(
            'logout',
            dict(user=shared.session['user']))
    else:
        return bottle.template(
            'login',
            dict(message=''))


@bottle.post('/login') # or @route('/login', method='POST')
def login_submit():
    username     = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    
    if check_user_credentials(username, password):
        shared.session['user'] = username
        return bottle.template('logout', dict(user=username))
    
    else:
        shared.session['user'] = None
        return bottle.template(
            'login',
            dict(message='Login failed. Try again:'))


@bottle.route('/restricted')
@bottle.view('page')
def restricted_area():
    username = shared.session['user']
    if username:
        return dict(
            content='Hello %s. Welcome.' % username,
            title='Restricted')
    else:
        return dict(
            content='You are not logged in. Access denied.',
            title='Restricted')
