#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseProviderBackend


class DictionaryProviderBackend(BaseProviderBackend):
    def __init__(self, dict, *args, **kwargs):
        super(DictionaryProviderBackend, self).__init__(*args, **kwargs)
        self._dict = dict or {}

    def get(self, key, default_value):
        try:
            return self._dict[key]
        except:
            return default_value

    def set(self, key, value):
        self._dict[key] = value

    def delete(self, key):
        if key in self._dict:
            del self._dict[key]

    def to_dict(self):
        return self._dict

# vim: filetype=python
