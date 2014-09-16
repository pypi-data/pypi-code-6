# -*- coding: utf-8 -*-
"""
Lime Light API clients
"""

from functools import partial

from . import membership, transaction


class BaseClient(object):
    """
    A Lime Light API client object.
    """
    def __init__(self, host=None, username=None, password=None):
        """
        :param host: Lime Light API endpoint
        :param username: Lime Light API username
        :param password: Lime Light API password/key/token
        """
        if all([host, username, password]):
            self.host = host
            self.username = username
            self.password = password
        else:
            raise ValueError('All arguments are required')


class MembershipClient(BaseClient):
    """
    The client object for accessing the Lime Light Membership API
    """
    def __getattr__(self, item):
        raise NotImplementedError
        #method_class = getattr(membership, item, None)
        #if method_class is None:
        #    raise AttributeError
        #return partial(method_class, host=self.host, username=self.username, password=self.password)


class TransactionClient(BaseClient):
    """
    The client object for accessing the Lime Light Transaction API
    """
    def __getattr__(self, item):
        method_class = getattr(transaction, item, None)
        if method_class is None:
            raise AttributeError
        return partial(method_class, host=self.host, username=self.username, password=self.password)