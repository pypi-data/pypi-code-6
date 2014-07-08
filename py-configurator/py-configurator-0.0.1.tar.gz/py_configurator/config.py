#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):
    def __init__(self, provider, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.provider = provider

    def get(self, name, default_value=None):
        return self.provider.get(name, default_value)

    def set(self, name, value):
        return self.provider.set(name, value)

    def delete(self, name):
        return self.provider.delete(name)

# vim: filetype=python
