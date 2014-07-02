""" goulash.cache

    dumb lightweight caching decorator.  this requires werkzeug,
    but at least avoids a memcache dependency.
"""

from functools import wraps

from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

def cached(key_or_fxn, timeout=5 * 60, use_request_vars=False):
    """ adapted from http://flask.pocoo.org/docs/patterns/viewdecorators/ """
    if use_request_vars:
        tmp1 = key_or_fxn
        assert isinstance(key_or_fxn, basestring)
        def cache_key_fxn():
            from flask import request
            req = request
            z = sorted(req.values.items())
            import json
            key = tmp1 + json.dumps(z)
            return key
    elif isinstance(key_or_fxn, basestring):
        cache_key_fxn = lambda: key_or_fxn
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            tmp2 = cache_key_fxn()
            rv = cache.get(tmp2)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(tmp2, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator
