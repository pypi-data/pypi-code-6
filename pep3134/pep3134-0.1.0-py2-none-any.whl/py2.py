# -*- coding: utf-8 -*-


import sys

from .utils import prepare_raise, construct_exc_class


# noinspection PyUnusedLocal
@prepare_raise
def raise_(type_, value=None, traceback=None):  # pylint: disable=W0613
    """
    Does the same as ordinary ``raise`` with arguments do in Python 2.
    But works in Python 3 (>= 3.3) also!

    Please checkout README on https://github.com/9seconds/pep3134
    to get an idea about possible pitfals. But short story is: please
    be pretty carefull with tracebacks. If it is possible, use sys.exc_info
    instead. But in most cases it will work as you expect.
    """

    prev_exc, prev_tb = sys.exc_info()[1:]
    proxy_class = construct_exc_class(type(type_))

    err = proxy_class(type_)
    err.__cause__ = None
    err.__suppress_context__ = False

    if getattr(prev_exc, "__pep3134__", False):
        prev_exc = prev_exc.with_traceback(prev_tb)
    err.__context__ = prev_exc

    if traceback:
        raise err.with_traceback(traceback), None, traceback
    else:
        raise err


def raise_from(exc, cause):
    """
    Does the same as ``raise LALALA from BLABLABLA`` does in Python 3.
    But works in Python 2 also!

    Please checkout README on https://github.com/9seconds/pep3134
    to get an idea about possible pitfals. But short story is: please
    be pretty carefull with tracebacks. If it is possible, use sys.exc_info
    instead. But in most cases it will work as you expect.
    """

    context_tb = sys.exc_info()[2]

    incorrect_cause = not (
        (isinstance(cause, type) and issubclass(cause, Exception)) or
        isinstance(cause, BaseException) or
        cause is None
    )
    if incorrect_cause:
        raise TypeError("exception causes must derive from BaseException")

    if cause is not None:
        if not getattr(cause, "__pep3134__", False):
            # noinspection PyBroadException
            try:
                raise_(cause)
            except:  # noqa pylint: disable=W0702
                cause = sys.exc_info()[1]
        cause.__fixed_traceback__ = context_tb

    # noinspection PyBroadException
    try:
        raise_(exc)
    except:  # noqa pylint: disable=W0702
        exc = sys.exc_info()[1]

    exc.__suppress_context__ = True
    exc.__cause__ = cause
    exc.__context__ = None

    raise exc
