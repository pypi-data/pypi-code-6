#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding:utf8

"""
Send a SSL request to the SightCall authentification API, with the key 
and certificate extracted from a p12 file.
"""

from os import path, makedirs
import urllib.request as request
import http.client, json

from sightcall_auth.config import directory

__all__ = ['Auth']

class HTTPSClientAuthHandler(request.HTTPSHandler):

    def __init__(self, key, cert):
        request.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        # Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return http.client.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)


class Auth():
    """
        :param client_id: The client ID of your provider
        :param client_secret: The client secret of your provider
        :param url: The url where the request will be sent
        :return: A token ready ot be used
        :rtype: str
    """
    client_id = None
    client_secret = None
    url = None

    def __init__(self, client_id, client_secret, url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url

    def connect(self, uid):
        https_con = HTTPSClientAuthHandler(directory + '/private_key.pem', directory + '/cert.pem')
        opener = request.build_opener(https_con)
        response = opener.open(path.join(self.url, "?client_id="+ self.client_id
                                            +"&client_secret="+ self.client_secret
                                            +"&uid="+ uid))
        return json.loads(response.read().decode("utf-8"))['token']

