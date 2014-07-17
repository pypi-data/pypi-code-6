# -*- coding: utf-8 -*-
'''
    flask.ext.flask_launchkey
    ---------------

    This module provides LaunchKey user authentication and session management
    with Flask utilizing the LaunchKey SDK and Flask-Login.

    :copyright: (c) 2014 LaunchKey, Inc.
    :license: MIT, see LICENSE for more details.
'''

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'Brad Porter'
__license__ = 'MIT'
__copyright__ = '(c) 2014 by LaunchKey'
__all__ = ['LaunchKeyManager']

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from flask import current_app, session

from flask.ext.login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)

import launchkey
from functools import wraps

class User(UserMixin):
    '''
    Custom user class to be used with flask-login
    '''
    def __init__(self, username, auth_request):
        self.id = username
        self.auth_request = auth_request

class LaunchKeyManager(object):
    '''
    Manager used to handle LaunchKey authentication as well as user sessions.
    '''

    def __init__(self, app=None, session_protection='strong', api_host='', test=False):
        '''
        Manager initialization
        :param app: Flask App.
        :param session_protection: String. A custom session protection can be set if strong is not desired.
               See https://flask-login.readthedocs.org/en/latest/#session-protection
        :param api_host: String. Custom LaunchKey API host. Safe to leave to default normally.
        '''
        self.app = app
        self.api_host = api_host
        self.test = test
        if app is not None:
            self.init_app(app, session_protection)

    def _test_API(self):
        private_key, public_key = launchkey.generate_RSA()
        self.public_key = public_key
        return launchkey.API(1234567890, "abcdefghijklmnopqrstuvwyz1234567", private_key,
                   "testdomain.com", "v1")

    def init_app(self, app, session_protection):
        '''
        App initialization
        '''
        app.login_manager = LoginManager(app)
        app.login_manager.session_protection = session_protection
        app.login_manager.user_callback = self._load_user

    @property
    def api(self):
        '''
        Launchkey API getter
        '''
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'launchkey_api'):
                if self.test:
                    ctx.launchkey_api = self._test_API()
                else:
                    # Pull all configuration from the app.config to create an API object
                    app_key = self.app.config.get('LAUNCHKEY_APP_KEY')
                    secret_key = self.app.config.get('LAUNCHKEY_SECRET_KEY')
                    private_key_path = self.app.config.get('LAUNCHKEY_PRIVATE_KEY_PATH')
                    private_key = open(private_key_path, "r").read()
                    ctx.launchkey_api = launchkey.API(app_key, secret_key, private_key, api_host=self.api_host)
            return ctx.launchkey_api

    @property
    def login_view(self):
        '''
        Returns login view
        '''
        return current_app.app.login_manager.login_view

    @login_view.setter
    def login_view(self, value):
        '''
        Allows setting login view
        :param: String. Uri path to login view.
        '''
        self.app.login_manager.login_view = value

    def _auth_in_progress(func):
        '''
        Session validation decorator
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'auth_request' in session and 'username' in session:
                return func(*args, **kwargs)
            else:
                return
        return wrapper

    def _load_user(self, username):
        '''
        Pulls the active Flask-Login user object
        :return: User object
        '''
        return User(session['username'], session['auth_request'])

    def authorize(self, username):
        '''
        Sends auth request to LaunchKey
        :param username: String. LaunchKey username for the request.
        :return: Bool. Authorization success based on whether the user exists.
        '''
        auth_request = self.api.authorize(username, session = True)
        
        # Check whether the user exists
        if "Error: " in auth_request:
            return False
        else:
            # Add content to the session so we can access it later
            session['auth_request'] = auth_request
            session['username'] = username
            return True

    @_auth_in_progress
    def poll_request(self):
        '''
        Polls LaunchKey for a user response
        :return: Bool. Statement on whether the user has responded.
        '''
        auth_response = self.api.poll_request(session['auth_request'])
        # A status code is returned if still waiting on user input
        if 'status_code' in auth_response:
            return False
        # Otherwise a user hash and auth key will be returned
        elif 'auth' in auth_response:
            session['auth_key'] = auth_response['auth']
            return True

    @_auth_in_progress
    def is_authorized(self):
        '''
        Checks if the user has been authorized
        :return: Bool. Success of authorization attempt.
        
        '''
        if self.api.is_authorized(session['auth_request'], session['auth_key']):
            return True
        else:
            return False

    @_auth_in_progress
    def login(self):
        '''
        Logs in the user
        :return: Bool. Success on whether the user was logged in.
        '''
        user = User(session['username'], session['auth_request'])
        login_user(user)
        return True

    @_auth_in_progress
    def logout(self):
        '''
        Deauthorizes the user from LaunchKey the server
        :return: Bool. Success of deauth.
        '''
        # Deauth from LaunchKey
        success = self.api.logout(session['auth_request'])
        # End Flask-Login session
        logout_user()
        # Clean up session
        session.pop('auth_request', None)
        session.pop('auth_key', None)
        session.pop('username', None)
        return success