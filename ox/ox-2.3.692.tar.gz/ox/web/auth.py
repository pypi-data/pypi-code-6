# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2009
from __future__ import print_function
import os

from ox.utils import json

def get(key):
    user_auth = os.environ.get('oxAUTH', os.path.expanduser('~/.ox/auth.json'))
    auth = {}
    if os.path.exists(user_auth):
        f = open(user_auth, "r")
        data = f.read()
        f.close()
        auth = json.loads(data)
    if key in auth:
        return auth[key]
    print("please add key %s to json file '%s'" % (key, user_auth))
    raise Exception,"no key %s found" % key

def update(key, value):
    user_auth = os.environ.get('oxAUTH', os.path.expanduser('~/.ox/auth.json'))
    auth = {}
    if os.path.exists(user_auth):
        f = open(user_auth, "r")
        data = f.read()
        f.close()
        auth = json.loads(data)
    auth[key] = value
    f = open(user_auth, "w")
    f.write(json.dumps(auth, indent=2))
    f.close()
    
