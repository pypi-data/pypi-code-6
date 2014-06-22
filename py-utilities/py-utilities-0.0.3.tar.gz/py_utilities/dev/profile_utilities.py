#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile
import functools
import pstats
import StringIO


def profile(sortby='cumulative'):  # pragma: no cover
    def _inner(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()
            retval = pr.runcall(func, *args, **kwargs)
            pr.disable()
            s = StringIO.StringIO()
            pstats.Stats(pr, stream=s).sort_stats(sortby).print_stats()
            print s.getvalue()
            return retval
        return _wrapper
    return _inner

# vim: filetype=python
