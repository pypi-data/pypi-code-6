#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-23 下午3:14


class Singleton(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls != type(cls.__instance):
            cls.__instance = object.__new__(cls, *args, **kwargs)
            cls.__instance.init_singleton()

        return cls.__instance

    def init_singleton(self):
        pass