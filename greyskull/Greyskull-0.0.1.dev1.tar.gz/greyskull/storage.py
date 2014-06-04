# -*- coding: utf-8 -*-
"""
Greyskull key storage
~~~~~~~~~~~~~~~~~~~~~

Currently memcached-only, eventual support for different key/value stores is planned.
"""

import os

from memcache import Client

SERVERS = os.getenv('GREYSKULL_MEMCACHED_ENDPOINTS', ['127.0.0.1:11211']),

if isinstance(SERVERS, str):
    SERVERS = SERVERS.split(',')
    if SERVERS[-1] == '':
        SERVERS = SERVERS[:-1]

mc = Client(['127.0.0.1:11211'], debug=0)


def _namespace_key(key: str, namespace: str or None) -> str:
    """

    """
    if namespace is not None:
        return '/'.join([namespace, key])
    else:
        return key


def get(key: str, namespace: str or None=None) -> str or None:
    """

    """
    return mc.get(_namespace_key(key, namespace))


def set(key: str, val, time=0, min_compress_len=0, namespace: str or None=None):
    """

    :param key:
    :param val:
    :param namespace:
    :return:
    """
    return mc.set(_namespace_key(key, namespace), val, time=time, min_compress_len=min_compress_len)


def get_multi(keys, key_prefix='', namespace=None):
    """

    :param keys:
    :param key_prefix:
    :param namespace:
    :return:
    """
    return mc.get_multi((_namespace_key(key, namespace) for key in keys), key_prefix=key_prefix)


def delete(key, time=0, namespace=None):
    """

    :param key:
    :param time:
    :param namespace:
    :return:
    """
    return mc.delete(_namespace_key(key, namespace), time=time)


def incr(key, delta=1, namespace=None):
    """

    :param key:
    :param delta:
    :param namespace:
    :return:
    """
    return mc.incr(_namespace_key(key, namespace), delta=delta)


def decr(key, delta=1, namespace=None):
    """

    :param key:
    :param delta:
    :param namespace:
    :return:
    """
    return mc.decr(_namespace_key(key, namespace), delta=delta)