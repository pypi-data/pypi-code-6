import logging
import random
import urllib

from . import accounts
from ._depend import HttpResponseRedirect, HostingServiceAccount


def build_url(baseurl, relpath, args=None):
    if relpath is None:
        relpath = ""
    url = baseurl + relpath
    if args:
        names = iter(sorted(args))
        # Handle the first one.
        name = next(names)
        value = urllib.quote(args[name], '')
        url = '{}?{}={}'.format(url, name, value)
        # Handle the rest (if any).
        for name in names:
            value = urllib.quote(args[name], '')
            url = '{}&{}={}'.format(url, name, value)
    return url


class ProviderInfo(object):

    SERVICE = None

    NAME = None
    BUTTON = None

    HOSTING_URL = None
    OAUTH_BASE = None
    INITIATE_PATH = None

    @property
    def name(self):
        if self.NAME is None:
            return self.SERVICE.name
        else:
            return self.NAME

    @property
    def id(self):
        return self.name.lower()

    @property
    def button(self):
        if self.BUTTON is None:
            return self.id
        else:
            return self.BUTTON

    def build_url(self, relpath, args=None, api=False):
        if api:
            base = self.service().get_api_url(self.HOSTING_URL)
            if base.endswith('/'):
                base = base[:-1]
        else:
            base = self.OAUTH_BASE
        return build_url(base, relpath, args)

    def build_account(self, username=None):
        account = HostingServiceAccount()
        account.service_name = self.id
        account.hosting_url = self.HOSTING_URL
        if username is not None:
            account.username = username
        return account

    def service(self, username=None):
        if self.SERVICE is None:
            return None
        account = self.build_account(username)
        return self.SERVICE(account)


class BaseProvider(object):

    INFO = None

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        return getattr(self.info, name)

    @property
    def info(self):
        try:
            return self._info
        except AttributeError:
            if self.INFO is None:
                return None
            self._info = self.INFO()
            return self._info

    def get_token(self, valetkey):
        """Return the OAuth token corresponding to the valet key."""
        raise NotImplementedError

    def get_account(self, token):
        """Return the corresponding HostingServiceAccount.
        
        This method should not save the account.

        """
        # XXX Use one of reviewboard's hosting service objects?
        raise NotImplementedError

    def initiate(self):
        """Return a Django response that redirects to the provider."""
        raise NotImplementedError

    def handle(self, request):
        """Return the username and OAuth token from the request."""
        raise NotImplementedError


class Provider(BaseProvider):

    AUTH_ID_BITS = 32

    SECURE_TOKEN_KEY = None
    CALLBACK_KEY = None

    VALET_KEY = None

    APP_ID_FIELD = None
    APP_ID_HELP = 'Your registered application ID'
    APP_SECRET_FIELD = None
    APP_SECRET_HELP = 'Your registered application secret key'

    @classmethod
    def add_settings(cls):
        #backend.add_provider_settings(cls)
        pass

    def __init__(self, authid=None, callback=None, next=None):
        super(Provider, self).__init__()
        if authid is None:
            authid = '{:0x}'.format(random.getrandbits(self.AUTH_ID_BITS))

        if callback is not None:
            if '?' in callback:
                callback += '&'
            else:
                callback += '?'
            # XXX drop authid from callback
            # XXX extrapolate provider from the request?
            callback += 'authid={}&provider={}'.format(authid, self.id)
            if next is not None:
                callback += '&next={}'.format(next)

        self.callback = callback
        self.authid = authid
        self.next = next

    @property
    def initiate_args(self):
        args = {}
        if self.SECURE_TOKEN_KEY is not None:
            args[self.SECURE_TOKEN_KEY] = self.authid
        if self.CALLBACK_KEY is not None and self.callback:
            args[self.CALLBACK_KEY] = self.callback
        return args

    def initiate(self):
        url = self.info.build_url(self.INITIATE_PATH, self.initiate_args)
        return HttpResponseRedirect(url)

    def handle(self, args):
        if self.SECURE_TOKEN_KEY is not None:
            if args[self.SECURE_TOKEN_KEY] != self.authid:
                raise RuntimeError('auth ID did not match')
        account = self.extract_remote_account(args)
        return account

    def get_or_create_account(self, token):
        account = self.get_account(token)
        existing = accounts.sync_existing(account)
        if existing is None:
            account.save()
            accounts.add_account_to_user(account)
            existing = account
            logging.debug('OAuth account created: {!r}'
                          .format(account.username))
        # We always update the token.
        accounts.set_token(existing, token)
        return existing

    def extract_remote_account(self, args):
        valetkey = args[self.VALET_KEY]
        token = self.get_token(valetkey)
        if token is None:
            return None
        account = self.get_or_create_account(token)
        return account
