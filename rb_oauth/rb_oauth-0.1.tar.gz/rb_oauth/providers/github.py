import json
import logging
import urlparse

from . import base, register
from ._depend import settings, GithubService, URLRequest, urlopen


class GithubInfo(base.ProviderInfo):

    SERVICE = GithubService

    OAUTH_BASE = 'https://github.com'
    INITIATE_PATH = '/login/oauth/authorize'


@register
class GithubProvider(base.Provider):

    INFO = GithubInfo

    TOKEN_PATH = '/login/oauth/access_token'
    USER_PATH = '/user'

    SECURE_TOKEN_KEY = 'state'
    CALLBACK_KEY = 'redirect_uri'

    VALET_KEY = 'code'

    @property
    def initiate_args(self):
        clientid = self.clientid
        if clientid is None:
            raise RuntimeError('settings.GITHUB_CLIENT_ID is not set')

        args = super(GithubProvider, self).initiate_args
        args['client_id'] = clientid
        return args

    @property
    def clientid(self):
        try:
            return settings.GITHUB_CLIENT_ID
        except AttributeError:
            return None

    def extract_auth(self, args):
        code = args['code']
        token = self.get_token(code)
        username = self.get_username(token)
        return username, token

    def _send_request(self, path, token, args=None, method='POST', api=False):
        if token is not None:
            if args is None:
                args = {}
            args['access_token'] = token
        # Build and send a POST request.
        url = self.build_url(path, args, api=api)
        headers = {'Accept': 'application/json'}
        req = URLRequest(url, headers=headers, method=method)
        resp = urlopen(req)
        if resp.getcode() != 200:
            raise Exception(resp.getcode())
            return None
        # Extract the token from the response.
        body = resp.read()
        return json.loads(body)

    def get_token(self, code):
        # Build and send a POST request.
        args = {'client_id': self.clientid,
                'client_secret': settings.GITHUB_CLIENT_SECRET,
                'code': code,
                }
        authinfo = self._send_request(self.TOKEN_PATH, None, args=args)
        if 'error' in authinfo:
            logging.debug('OAuth error: {}'.format(authinfo))
            return None
        return authinfo['access_token']

    def get_account(self, token):
        info = self._send_request(self.USER_PATH, token, method='GET', api=True)

        username = info['login']
        return self.info.build_account(username)
