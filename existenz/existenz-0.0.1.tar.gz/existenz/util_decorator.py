"""Utility decorators."""
from decorator import decorator


@decorator
def memoize(f):
    """A args based function cache."""
    memo = {}

    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = f(*args)
            memo[args] = rv
            return rv

    return wrapper
