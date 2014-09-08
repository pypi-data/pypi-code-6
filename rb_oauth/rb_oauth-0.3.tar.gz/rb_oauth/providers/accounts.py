import logging

from . import REGISTRY as _registry
from ._depend import User, HostingServiceAccount


PW_PREFIX = 'oauth:'


def encode_password(provider, username=None):
    if username is None:
        return PW_PREFIX + provider
    else:
        return '{}{}@{}'.format(PW_PREFIX, username, provider)


def decode_password(password):
    if not password.startswith(PW_PREFIX):
        return None
    username, at, provider = password[len(PW_PREFIX):].partition('@')
    if not at:
        provider, username = username, provider
    return provider, username
    

def get_account(accountname, service):
    if not accountname or not service:
        return None

    # For now we just piggyback on HostingServiceAccount.
    accounts = HostingServiceAccount.objects.filter(username=accountname,
                                                    service_name=service)
    if not accounts:
        return None
    try:
        account, = accounts
    except ValueError:
        raise RuntimeError('more than one account matches ({})'
                           .format(accountname))
    return account


def sync_existing(account):
    existing = get_account(account.username, account.service_name)
    if existing is None:
        return None
    # XXX Compare account to existing
    return existing


def get_token(account):
    try:
        auth = account.data['authorization']
    except KeyError:
        return None
    else:
        return auth.get('oauth_token')


def set_token(account, token, save=True):
    try:
        auth = account.data['authorization']
    except KeyError:
        auth = account.data['authorization'] = {}
    auth['oauth_token'] = token
    if save:
        account.save()


def add_account_to_user(account):
    # XXX Finish it.
    # Find matching user.
    # Associate account with user.
    pass


def extract_provider_and_account(password, username):
    # Extract the provider and account names.
    providerinfo = decode_password(password)
    if not providerinfo:
        raise NotImplementedError('could not decode password')
    providername, accountname = providerinfo
    if not accountname:
        accountname = username

    # Get the provider.
    try:
        cls = _registry[providername]
    except KeyError:
        raise NotImplementedError('unknown OAuth provider: {!r}'
                                  .format(providername))
    provider = cls()

    # Get the account.
    account = get_account(accountname, providername)

    return provider, account


def authenticate(provider, account):
    # Pull the stored token.
    token = get_token(account)
    if not token:
        logging.debug('account not registered: {!r}'
                      .format(account.username))
        return None

    # Use the token to pull the remote account.
    actual = provider.get_account(token)
    if not actual:
        logging.debug('account not available remotely: {!r}'
                      .format(account.username))
        return None

    return actual


def get_or_create_user(username):
    user, is_new = User.objects.get_or_create(username=username)
    if is_new:
        logging.debug('created new user: {!r}'.format(username))
        user.set_unusable_password()
        user.save()
    return user
