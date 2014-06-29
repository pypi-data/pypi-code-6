# -*- coding: utf-8 -*-

from py3oauth2.interfaces import (
    ClientType,
    IAccessToken,
    IAuthorizationCode,
    IClient,
    IStore,
)


__all__ = ['ClientType', 'IAccessToken', 'IAuthorizationCode', 'IClient',
           'IStore']


class IClient(IClient):

    def get_jws_alg(self):
        raise NotImplementedError

    def get_jwe_alg(self):
        raise NotImplementedError

    def get_jwe_enc(self):
        raise NotImplementedError


class IOwner:

    def get_user_info(self, scopes):
        raise NotImplementedError

    def get_sub(self):
        raise NotImplementedError


class IStore(IStore):

    def get_signing_key(self, client):
        raise NotImplementedError

    def get_encrypting_key(self, client):
        raise NotImplementedError
