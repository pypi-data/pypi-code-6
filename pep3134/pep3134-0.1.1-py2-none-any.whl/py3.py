# -*- coding: utf-8 -*-


from .utils import prepare_raise


# noinspection PyUnusedLocal
@prepare_raise
def raise_(type_, value=None, traceback=None):
    """
    Does the same as ordinary ``raise`` with arguments do in Python 2.
    But works in Python 3 (>= 3.3) also!

    Please checkout README on https://github.com/9seconds/pep3134
    to get an idea about possible pitfals. But short story is: please
    be pretty carefull with tracebacks. If it is possible, use sys.exc_info
    instead. But in most cases it will work as you expect.
    """

    if type_.__traceback__ is not traceback:
        raise type_.with_traceback(traceback)
    raise type_


def raise_from(error, cause):
    """
    Does the same as ``raise LALALA from BLABLABLA`` does in Python 3.
    But works in Python 2 also!

    Please checkout README on https://github.com/9seconds/pep3134
    to get an idea about possible pitfals. But short story is: please
    be pretty carefull with tracebacks. If it is possible, use sys.exc_info
    instead. But in most cases it will work as you expect.
    """

    raise error from cause
