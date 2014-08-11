#!/usr/bin/env python

import json
import os
from hashlib import sha256

from flask import request, current_app
from flask.ext import restful
from flask.ext.restful import fields, abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

token_field = {
    'auth_token': fields.String
    }

class TokenResource(restful.Resource):
    """
    This resources is used to manage token. POST is used to create one
    """
    @restful.marshal_with(token_field)
    def post(self):
        """
        This is used by a client to obtain an auth-token. The client must
        provide in the body of the request its token-id.
        """
        # Let's get the token list and the token
        token_list = json.load(open(os.path.abspath(current_app.config['TOKEN_LIST'])))
        token_id = request.get_json()['token']

        # Our token must be present in our list, and the list is sha256 hashes.
        if not sha256(token_id).hexdigest() in token_list:
            abort(401, message="Invalid token-id provided")

        # Our token exist, so far so good. Now, let's send a signature and an
        # auth-token. It will be needed to sign content for authorisation
        # decorators and it will expires in two hours.
        s = Serializer(current_app.config['PRIVATE_KEY'], expires_in=7200)
        auth_token = s.dumps({'token_id': token_id})

        return {'auth_token': auth_token}
