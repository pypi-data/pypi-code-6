# -*- coding: utf-8 -*-


from .utils import prepare_raise


# Precompiled code for raise_from function and exec clause.
PRECOMPILED_RAISE = compile("raise error from cause", __file__, "exec")


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

    if type_.__traceback__ is not traceback:
        raise type_.with_traceback(traceback)
    raise type_


def raise_from(error, cause):  # pylint: disable=W0613
    """
    Does the same as ``raise LALALA from BLABLABLA`` does in Python 3.
    But works in Python 2 also!

    Please checkout README on https://github.com/9seconds/pep3134
    to get an idea about possible pitfals. But short story is: please
    be pretty carefull with tracebacks. If it is possible, use sys.exc_info
    instead. But in most cases it will work as you expect.
    """

    # Okay, this is a story on Python packaging. First, there were
    # just a simple generic version
    #
    # raise error from cause
    #
    # and it was good. It worked on my machine but for some reason
    # during the package installation within Python 2 this file
    # was parsed and of curse blowed up on syntax error. So I need
    # to implement this line but in a dynamic way

    exec(PRECOMPILED_RAISE, globals(), locals())  # pylint: disable=W0122
