# -*- coding: utf-8 -*-
# decorators.py
# Copyright (C) 2013 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Useful decorators.
"""
import collections
import datetime
import functools
import logging

logger = logging.getLogger(__name__)


class _memoized(object):
    """
    Decorator.

    Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """

    # cache invalidation time, in seconds
    CACHE_INVALIDATION_DELTA = 1800

    def __init__(self, func, ignore_kwargs=None, is_method=False,
                 invalidation=None):

        """
        :param ignore_kwargs: If True, ignore all kwargs.
                              If tuple, ignore those kwargs.
        :type ignore_kwargs: bool, tuple or None
        :param is_method: whether the decorated function is a method.
                          (ignores the self argument if so).
        :type is_method: True
        """
        self.ignore_kwargs = ignore_kwargs if ignore_kwargs else []
        self.is_method = is_method
        self.func = func

        if invalidation:
            self.CACHE_INVALIDATION_DELTA = invalidation

        # TODO should put bounds to the cache dict so we do not
        # consume a huge amount of memory.
        self.cache = {}
        self.cache_ts = {}

    def __call__(self, *args, **kwargs):
        """
        Executes the call.

        :tyoe args: tuple
        :type kwargs: dict
        """
        def ret_or_raise(value):
            """
            Returns the value except if it is an exception,
            in which case it's raised.
            """
            if isinstance(value, Exception):
                raise value
            return value

        if self.is_method:
            # forget about `self` as key
            key_args = args[1:]
        else:
            key_args = args

        if self.ignore_kwargs is True:
            key = key_args
        else:
            key = (key_args, frozenset(
                [(k, v) for k, v in kwargs.items()
                 if k not in self.ignore_kwargs]))

        if not isinstance(key, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            logger.warning("Key is not hashable, bailing out!")
            return self.func(*args, **kwargs)

        if key in self.cache:
            if self._is_cache_still_valid(key):
                value = self.cache[key]
                logger.debug("Got value from cache...")
                return ret_or_raise(value)
            else:
                logger.debug("Cache is invalid, evaluating again...")

        # no cache, or cache invalid
        try:
            value = self.func(*args, **kwargs)
        except Exception as exc:
            logger.error("Exception while calling function: %r" % (exc,))
            value = exc
        self.cache[key] = value
        self.cache_ts[key] = datetime.datetime.now()
        return ret_or_raise(value)

    def _is_cache_still_valid(self, key, now=datetime.datetime.now):
        """
        Returns True if the cache value is still valid, False otherwise.

        For now, this happen if less than CACHE_INVALIDATION_DELTA seconds
        have passed from the time in which we recorded the cached value.

        :param key: the key to lookup in the cache
        :type key: hashable
        :param now: a callable that returns a datetime object. override
                    for dependency injection during testing.
        :type now: callable
        :rtype: bool
        """
        cached_ts = self.cache_ts[key]
        delta = datetime.timedelta(seconds=self.CACHE_INVALIDATION_DELTA)
        return (now() - cached_ts) < delta

    def __repr__(self):
        """
        Return the function's docstring.
        """
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """
        Support instance methods.
        """
        return functools.partial(self.__call__, obj)


def memoized_method(function=None, ignore_kwargs=None):
    """
    Wrap _memoized to allow for deferred calling

    :type function: callable, or None.
    :type ignore_kwargs: None, True or tuple.
    """
    if function:
        return _memoized(function, is_method=True)
    else:
        def wrapper(function):
            return _memoized(
                function, ignore_kwargs=ignore_kwargs, is_method=True)
        return wrapper
