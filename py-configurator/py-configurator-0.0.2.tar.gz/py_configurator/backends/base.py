#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


class ConfigException(Exception):
    pass


class BaseProviderBackend(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super(BaseProviderBackend, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def get(self, key, default_value):
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, key, value):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    def to_dict(self, key):
        raise NotImplementedError


class FileProviderBackend(BaseProviderBackend):
    def __init__(self, file_path, *args, **kwargs):
        super(FileProviderBackend, self).__init__(*args, **kwargs)
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path


# vim: filetype=python
