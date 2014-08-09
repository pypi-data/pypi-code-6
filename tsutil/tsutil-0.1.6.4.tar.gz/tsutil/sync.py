#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This is from the Python Cookbook 9.1 about synchronization object and all its methods.
#
# @Author: Turbidsoul Chen
# @Date:   2014-08-09 16:02:59
# @Last Modified by:   Turbidsoul Chen
# @Last Modified time: 2014-08-09 16:07:22

import inspect


def wrap_object(func, before, after):
    '''
    before/after call will encapsulate callable object
    '''
    def _wrapper(*args, **kwargs):
        before()
        try:
            return func(*args, **kwargs)
        except Exception, e:
            raise e
        finally:
            after()
    return _wrapper


class GenericWrapper(object):
    """
    object of all methods use before/after calls to encapsulate
    """
    def __init__(self, obj, before, after, ignore={}):
        clazzname = 'GenericWrapper'
        self.__dict__['_%s__method' % clazzname] = {}
        self.__dict__['_%s__obj' % clazzname] = obj
        for name, method in inspect.getmembers(obj, inspect.ismethod):
            if name not in ignore and method not in ignore:
                self.__method[name] = wrap_object(method, before, after)

    def __getattr__(self, name):
        try:
            return self.__methods[name]
        except Exception:
            return getattr(self.__obj, name)

    def __setattr__(self, name, value):
        setattr(self.__obj, name, value)


class SynchronizedObject(GenericWrapper):
    '''
    Synchronized Object
    '''
    def __init__(self, obj, ignore={}, lock=None):
        if not lock:
            import threading
            lock = threading.RLock()
        GenericWrapper.__init__(self, obj, lock.acquire, lock.release, ignore)