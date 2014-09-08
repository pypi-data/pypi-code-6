import json
import logging
import urlparse

from . import base, register
from ._depend import (settings, GithubService, URLRequest, urlopen,
                      SiteConfiguration)


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

    APP_ID_SETTING = 'GITHUB_CLIENT_ID'
    APP_SECRET_SETTING = 'GITHUB_CLIENT_SECRET'

    def _get_app_info(self, kind):
        key = 'auth_oauth_app_{}_{}'.format(kind.lower(), self.name)
        # Try the DB first.
        try:
            siteconfig = SiteConfiguration.objects.get_current()
        except Exception:
            siteconfig = None
        else:
            value = siteconfig.get(key)
            if value:
                return value

        # Fall back to settings.
        try:
            setting = getattr(self, 'APP_{}_SETTING'.format(kind.upper()))
            value = getattr(settings, setting)
        except AttributeError:
            return None

        # Cache the value.
        if siteconfig is not None:
            siteconfig.set(key, value)

        return value

    @property
    def app_id(self):
        """The provider-registered ID to use for OAuth requests."""
        return self._get_app_info('id')

    @property
    def app_secret(self):
        """The provider-provided private key to use for OAuth requests."""
        return self._get_app_info('secret')

    @property
    def initiate_args(self):
        clientid = self.app_id
        if clientid is None:
            raise RuntimeError('settings.GITHUB_CLIENT_ID is not set')

        args = super(GithubProvider, self).initiate_args
        args['client_id'] = clientid
        return args

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
        args = {'client_id': self.app_id,
                'client_secret': self.app_secret,
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
