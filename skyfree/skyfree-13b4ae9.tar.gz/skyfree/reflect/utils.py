#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-23 下午2:20
import sys
import traceback


def import_class(import_str):
    """
    根据字符串导入某个class
    :param import_str: 类全名，例如skyfree.a.AClass
    :return: 返回AClass的类对象 :raise ImportError: 没找到类
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    try:
        __import__(mod_str)
        return getattr(sys.modules[mod_str], class_str)
    except (ValueError, AttributeError):
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))


def import_object(import_str, *args, **kwargs):
    """

    :param import_str: 类全名
    :param args: 类的初始化参数
    :param kwargs: 类的初始化参数
    :return: 对象实例
    """
    return import_class(import_str)(*args, **kwargs)


def import_object_ns(name_space, import_str, *args, **kwargs):
    import_value = "%s.%s" % (name_space, import_str)
    try:
        return import_class(import_value)(*args, **kwargs)
    except ImportError:
        return import_class(import_str)(*args, **kwargs)


def import_module(import_str):
    """导入一个模块"""
    __import__(import_str)
    return sys.modules[import_str]


def try_import(import_str, default=None):
    """尝试导入一个模块，如果失败了返回default值"""
    try:
        return import_module(import_str)
    except ImportError:
        return default