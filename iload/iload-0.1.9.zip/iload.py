# -*- coding: utf-8 -*-
import sys
import importlib
import inspect


try:
    reload
except NameError:
    try:
        from imp import reload
    except ImportError:
        from importlib import reload


def iload(name):
    try:
        return importlib.import_module(name)
    except ImportError:
        mod_name, obj_name = name.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        return getattr(mod, obj_name)


def ireload(obj, mod=None):
    # 对于模块，直接加载
    if inspect.ismodule(obj):
        return reload(obj)

    # 处理明确指定了模块的情况
    if mod:
        obj_name = getattr(obj, '__name__', obj)
        mod = ireload(mod)
        return getattr(mod, obj_name)

    # 重新加载对象
    mod_name = getattr(obj, '__module__', None)
    mod = sys.modules[mod_name]
    return ireload(obj, mod)
