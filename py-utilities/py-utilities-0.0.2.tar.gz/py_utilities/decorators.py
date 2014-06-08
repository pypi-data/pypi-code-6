#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools


def apply(func_to_apply):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func_to_apply(func(*args, **kwargs))
        return wrapper
    return decorator


def run_once(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def safe(func, exceptions_to_catch=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if exceptions_to_catch:
                try:
                    return func(*args, **kwargs)
                except exceptions_to_catch:
                    return None
            else:
                try:
                    return func(*args, **kwargs)
                except:
                    return None
        return wrapper
    return decorator

# vim: filetype=python
