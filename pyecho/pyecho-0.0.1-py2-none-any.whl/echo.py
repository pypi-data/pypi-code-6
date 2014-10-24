"""
           _
  ___  ___| |__   ___
 / _ \/ __| '_ \ / _ \
|  __/ (__| | | | (_) |
 \___|\___|_| |_|\___/

author: Nauman Ahmad
description: A micro library for retrying failing operations.
version: 0.0.1
license: MIT
"""
from functools import wraps


class FailingTooHard(Exception):
    pass


def parametrized(dec):
    """Makes the decorator take arguments"""
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


@parametrized
def echo(f, retries):
    @wraps(f)
    def wrapper(*args, **kwargs):
        i = 0
        while i < retries:
            try:
                return f(*args, **kwargs)
            except Exception as e:
                i += 1
                if retries == i:
                    raise FailingTooHard(e)
    return wrapper
