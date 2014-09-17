# -*- coding: utf-8 -*-
"""
    tlutil.cache
"""


import cPickle
import inspect

from functools import wraps


__all__ = [
    "rc_cached", "mc_cached"
]


def _gen_key(pattern, names, args):
    values = args[:len(names)]
    replaces = dict(zip(names, values))
    return pattern.format(**replaces)


def rc_cached(rc, pattern, timeout=0):
    """redis缓存包装器
    :param rc: redis client
    :param pattern: 缓存模式 `rc:video:{video_id}`
    :param timeout: 超时时间
    """
    def decorator(f):
        @wraps(f)
        def run(*args, **kwargs):
            argspec = inspect.getargspec(f)
            if argspec.varargs or argspec.keywords:
                raise Exception("not support args or kwargs")
            name = _gen_key(pattern, argspec.args, args)
            response = rc.get(name)
            if response is None:
                response = f(*args, **kwargs)
                rc.set(name, cPickle.dumps(response))
                if timeout:
                    rc.expire(name, timeout)
            else:
                response = cPickle.loads(response)
            return response
        return run
    return decorator


def mc_cached(mc, pattern, timeout=600):
    """memcached缓存包装器
    :param mc: memcached client
    :param pattern: 缓存模式 `rc:video:{video_id}`
    :param timeout: 超时时间
    """
    def decorator(f):
        @wraps(f)
        def run(*args, **kwargs):
            argspec = inspect.getargspec(f)
            if argspec.varargs or argspec.keywords:
                raise Exception("not support args or kwargs")
            name = _gen_key(pattern, argspec.args, args)
            response = mc.get(name)
            if response is None:
                response = f(*args, **kwargs)
                mc.set(name, response, timeout)
            return response
        return run
    return decorator
