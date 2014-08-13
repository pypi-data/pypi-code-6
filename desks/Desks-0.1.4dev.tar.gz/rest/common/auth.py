#!/usr/bien/env python

import json
import os
import datetime
import functools
from hashlib import sha256

from flask import request, current_app
from flask.ext import restful
from flask.ext.restful import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
"""
This module will be used to auth and provide method decorators to check access right.
The creation of the token will be managed by a specific resource.
"""

def authenticate(func):
    """
    This is a decorator, whch will test if the current request is correctly
    authenticated. The request parameters must include a token and a timestamp
    and a signature which is a HMAC of the timestamp by the token.

    The token should be a valid HMAC generated with our private key, and once
    decoded, we should have an auth-token from our tokenlist.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Fisrt we need to check we have the correct values
        if not set(['timestamp', 'sig', 'token']) <= set(request.values.keys()):
            # We lack at least one of the args:
            abort(401, message="Missing %s" % (set(['timestamp', 'sig', 'token']) - set(request.values.keys()),))

        # We need to check if the token is correct
        s = Serializer(current_app.config['PRIVATE_KEY'])
        try:
            token_id = s.loads(request.values['token'])['token_id']
        except BadSignature:
            abort(401, message="Invalid auth-token %s" %(request.values['token'],))
        except SignatureExpired:
            abort(401, message="Auth-token expired, ask for another one.")

        with open(os.path.abspath(current_app.config['TOKEN_LIST'])) as f:
            token_list = json.load(f)

        if not sha256(token_id).hexdigest() in token_list:
            abort(401, message="No id associated to this auth-token: %s" % request.values['token'])

        # We do have a valid auth-token associated to a value token-id, and this
        # token-id exists.
        # We now need to check if the signature is correct. It must have been done
        # using the token_id and the timestamp.
        s = Serializer(unicode(token_id))
        try:
            signed_timestamp = s.loads(request.values['sig'])
        except BadSignature:
            abort(401, message="Bad signature of query %s" % (request.values['sig'],))
        except BadData:
            abort(401, message="Bad data for query %s" % (request.values['sig'],))


        # If the signed_timestamp and the one in the request differs, something is
        # wrong
        if signed_timestamp != request.values['timestamp']:
            abort(401, message="Incorrect value for signature %s with timestamp: %s (encoded: %s)" % (request.values['sig'], request.values['timestamp'], signed_timestamp))

        # If signed_timestamp is in the future or more than 5 min old, then
        # It's probably a forged packet.
        now = datetime.datetime.now()
        ts = datetime.datetime.fromtimestamp(float(signed_timestamp))
        if now < ts or now - datetime.timedelta(minutes=5) >= ts:
            # We're lost in time
            abort(401, message="timestamp do not match reality of time")

        # If we're here, everything is ok
        return func(*args, **kwargs)
    return wrapper
