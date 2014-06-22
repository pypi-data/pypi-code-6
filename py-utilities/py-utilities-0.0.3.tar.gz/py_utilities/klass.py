#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp
import importlib
import inspect
import os


def get_klass_from_str(klass_as_str):
    """
    Returns a klass from a string

    >>> get_klass_from_str('Queue.Queue') #doctest: +ELLIPSIS
    <class Queue.Queue at 0x...>

    >>> get_klass_from_str('Queue.Queue')() #doctest: +ELLIPSIS
    <Queue.Queue instance at 0x...>

    """
    return _get_klass_or_func_from_str_impl(klass_as_str,
                                            lambda x: inspect.isclass(x))


def get_func_from_str(func_as_str):
    """
    Returns a function from a string

    >>> get_func_from_str('Queue.Queue')

    >>> get_func_from_str('Queue.Queue')() #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: 'NoneType' object is not callable

    >>> get_func_from_str('math.fsum')
    """
    return _get_klass_or_func_from_str_impl(func_as_str,
                                            lambda x: inspect.isfunction(x))


def get_klass_from_file(path_to_file, klass_as_str):
    """
    Returns a klass from a file (compiled or not)
    """
    return _get_klass_or_func_from_file_impl(path_to_file, klass_as_str,
                                             lambda x: inspect.isclass(x))


def get_func_from_file(path_to_file, func_as_str):
    """
    Returns a function from a file (compiled or not)
    """
    return _get_klass_or_func_from_file_impl(path_to_file, func_as_str,
                                             lambda x: inspect.isfunction(x))


def _get_klass_or_func_from_str_impl(klass_or_func_as_str, lambda_test):
    module_name, kfun_name = klass_or_func_as_str.rsplit(".", 1)
    module = importlib.import_module(module_name)
    kfun = getattr(module, kfun_name) if hasattr(module, kfun_name) else None
    return kfun if kfun and lambda_test(kfun) else None


def _get_klass_or_func_from_file_impl(path_to_file, klass_or_fun_as_str,
                                      lambda_test):

    module_name, file_ext = os.path.splitext(os.path.split(path_to_file)[-1])

    if file_ext.lower() == '.py':
        module = imp.load_source(module_name, path_to_file)
    elif file_ext.lower() == '.pyc':
        module = imp.load_compiled(module_name, path_to_file)

    kfun = getattr(module, klass_or_fun_as_str) \
        if hasattr(module, klass_or_fun_as_str) else None

    return kfun if kfun and lambda_test(kfun) else None

# vim: filetype=python
