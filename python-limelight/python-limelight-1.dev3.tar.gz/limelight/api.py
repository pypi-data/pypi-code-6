# -*- coding: utf-8 -*-

from .utils import not_implemented
from . import membership, transaction


class BaseClient(object):
    """
    A Lime Light API client object.
    """
    __method_package = not_implemented

    def __init__(self, host=None, username=None, password=None):
        if all([host, username, password]):
            self.host = host
            self.username = username
            self.password = password
        else:
            raise ValueError('All arguments are required')

    def __getattr__(self, item):
        method_class = getattr(self.__method_package, item, None)
        if method_class is None:
            raise AttributeError
        setattr(method_class, 'host', self.host)
        setattr(method_class, 'username', self.username)
        setattr(method_class, 'password', self.password)
        return method_class


class MembershipClient(BaseClient):
    __method_package = membership


class TransactionClient(BaseClient):
    __method_package = transaction