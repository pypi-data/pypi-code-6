'''
Created on May 9, 2014

@author: lwoydziak
'''
from jsonconfigfile import Env
from os import environ

def test_ConfigFile():
    initialJson = '{ \
        "iCloud" : { \
            "login"          : "None", \
            "password"       : "None", \
            "url"            : "http://www.icloud.com" \
        },\
        "Google" : { \
            "username"       : "None", \
            "password"       : "None", \
            "url"            : "http://calendar.google.com" \
        },\
        "sample" : "forTest"\
    }'
    environ.setdefault("garbage", "")
    Env(initialJson, "garbage", "garbage")
    assert Env().get("sample") == "forTest"
    assert Env().get("iCloud", "login") == "None"
    assert Env().get("garbage") == ''
    Env().envConfigFileNameOverride("envConfigFileNameOverride") 
    Env().load()
