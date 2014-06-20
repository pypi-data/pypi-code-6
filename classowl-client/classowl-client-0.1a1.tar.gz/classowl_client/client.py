from __future__ import unicode_literals
import requests
import slumber
from .serializer import Serializer

default_url = 'https://www.classowl.com/api/v1/'


class OAuth(requests.auth.AuthBase):
    """
    sets the OAuth authorization header to token;
    if token is not given makes a request to login
    with username and password to get it
    """
    token = None
    username = None
    password = None
    url = None

    def __init__(self, url=None, username=None, password=None, token=None):
        if token is None and (username is None or password is None or url is None):
            raise ValueError('you must provide a token or a username and a password')
        self.url = url
        self.username = username
        self.password = password
        self.token = token

    def __call__(self, r):
        if self.token is None:
            self.token = get_token(self.username, self.password, self.url)
        r.headers['Authorization'] = 'OAuth %s' % self.token
        return r


def get_token(username, password, base_url=default_url):
    """
    makes a login call to get an access token
    """
    try:
        response = slumber.API(base_url).login.post(data={'username': username,
                                                          'password': password})
    except slumber.exceptions.HttpClientError:
        raise ValueError('wrong username or password')
    return response['access_token']


def create_client(username=None, password=None, token=None, url=default_url):
    """
    create an api client authenticating with
    either token or username and password
    """
    serializer = Serializer()
    client = slumber.API(url,
                         auth=OAuth(url, username, password, token),
                         serializer=serializer)
    serializer.set_client(client)
    return client
