#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .base import ConfigException
from .base import FileProviderBackend
import yaml


class YamlProviderBackend(FileProviderBackend):
    def __init__(self, file_path, *args, **kwargs):
        super(YamlProviderBackend, self).__init__(file_path, *args, **kwargs)
        try:
            with open(file_path, 'r') as f:
                self._config = yaml.load(f)
        except Exception as e:
            raise ConfigException(e)

    def get(self, key, default_value=None):
        try:
            return self._get(self._config, key)
        except:
            return default_value

    def _get(self, target, key):
        if '.' not in key:
            return target[key]
        key, rest_of_key = key.split('.', 1)
        return self._get(target[key], rest_of_key)

    def set(self, key, value):
        try:
            return self._set(self._config, key, value)
        except Exception as e:
            raise ConfigException(e)

    def _set(self, target, key, value):
        if '.' not in key:
            target[key] = value
            return
        key, rest_of_key = key.split('.', 1)
        return self._set(target[key], rest_of_key, value)

    def delete(self, key):
        try:
            self._delete(self._config, key)
        except Exception as e:
            raise ConfigException(e)

    def _delete(self, target, key):
        if '.' not in key:
            del target[key]
            return
        key, rest_of_key = key.split('.', 1)
        return self._delete(target[key], rest_of_key)

    def to_dict(self):
        raise NotImplementedError

# vim: filetype=python
