# -*- coding: utf-8 -*-


import copy
import sys
import functools


def construct_exc_class(cls):
    """Constructs proxy class for the exception."""

    class ProxyException(cls, BaseException):
        __pep3134__ = True

        @property
        def __traceback__(self):
            if self.__fixed_traceback__:
                return self.__fixed_traceback__

            current_exc, current_tb = sys.exc_info()[1:]
            if current_exc is self:
                return current_tb

        def __init__(self, instance=None):
            super(ProxyException, self).__init__()

            self.__original_exception__ = instance
            self.__fixed_traceback__ = None

        def __getattribute__(self, item):
            if item == "__class__":
                return type(self.__original_exception__)
            return super(ProxyException, self).__getattribute__(item)

        def __repr__(self):
            return repr(self.__original_exception__)

        def with_traceback(self, traceback):
            instance = copy.copy(self)
            instance.__fixed_traceback__ = traceback
            return instance

    ProxyException.__name__ = cls.__name__

    return ProxyException


def prepare_raise(func):
    """
    Just a short decorator which shrinks
    full ``raise (E, V, T)`` form into proper ``raise E(V), T``.
    """

    @functools.wraps(func)
    def decorator(type_, value=None, traceback=None):
        if value is not None and isinstance(type_, Exception):
            raise TypeError("instance exception may not have a separate value")

        if value is None:
            if isinstance(type_, Exception):
                error = type_
            else:
                error = type_()
        else:
            error = type_(value)
        func(error, value, traceback)

    return decorator
