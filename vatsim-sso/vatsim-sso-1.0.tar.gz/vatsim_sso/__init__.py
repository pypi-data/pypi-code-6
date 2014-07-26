__author__ = 'Nick Harasym 1115151'

from requests_oauthlib import OAuth1
import requests


class VatsimSSO():

    def __init__(self, consumer_key, consumer_secret, signature_method='RSA-SHA1', callback_uri=None,
                 rsa_location=None, verifier=None, token=None, oauth_allow_suspended=0, oauth_allow_inactive=0):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.rsa_location = rsa_location
        self.call_backuri = callback_uri
        self.base_url = 'https://cert.vatsim.net/sso/api/'
        self.verifier = verifier
        self.token = token
        self.signature_method = signature_method
        self.oauth_allow_suspended = oauth_allow_suspended
        self.request_token = None
        self.oauth_allow_inactive = oauth_allow_inactive

    def login_token(self):
        extra_params = {'oauth_allow_suspended': self.oauth_allow_suspended,
                        'oauth_allow_inactive': self.oauth_allow_inactive}

        if self.signature_method == 'RSA-SHA1':
            prepare = OAuth1(self.consumer_key, client_secret=self.consumer_secret, callback_uri=self.call_backuri,
                             signature_method='RSA-SHA1',
                             rsa_key=open(self.rsa_location).read(), signature_type='query', verifier=None,)
        else:
            prepare = OAuth1(self.consumer_key, client_secret=self.consumer_secret, callback_uri=self.call_backuri,
                             signature_method='HMAC-SHA1', signature_type='query')
        request = requests.post(self.base_url + 'login_token/', auth=prepare, params=extra_params).json()

        self.request_token = request['token']['oauth_token']

        return str(self.request_token)

    def login_return(self):

        if self.verifier is None:
            return 'Please provide verifier'

        if self.token is None:
            return 'Please provide token'
        if self.signature_method == 'RSA-SHA1':
            prepare = OAuth1(self.consumer_key, client_secret=self.consumer_secret, signature_method='RSA-SHA1',
                             rsa_key=open(self.rsa_location).read(), verifier=self.verifier,
                             resource_owner_key=self.token, signature_type='query')
        else:
            prepare = OAuth1(self.consumer_key, client_secret=self.consumer_secret, signature_method='HMAC-SHA1',
                             verifier=self.verifier, resource_owner_key=self.token, signature_type='query')
        request = requests.post(self.base_url + 'login_return/', auth=prepare).json()
        return request