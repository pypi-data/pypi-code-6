"""Utility decorators."""
from decorator import decorator


def memoize(func):
    """Decorator to add cache to function calls.

    :param func: The function to be decorated with a cache.
    :type func: types.MethodType
    :return: The decorated function.
    :rtype: types.MethodType
    """
    func.cache = {}
    return decorator(_memoize, func)


def _memoize(func, *args, **kwargs):
    """A args based function cache."""
    if kwargs:
        key = args, frozenset(kwargs.iteritems())
    else:
        key = args
    cache = func.cache
    if key in cache:
        return cache[key]
    else:
        cache[key] = result = func(*args, **kwargs)
        return result
