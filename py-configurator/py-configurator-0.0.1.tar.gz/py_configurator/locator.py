#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .backends import get_provider
from .config import Config
import os


class Locator(object):
    def __init__(self, env_key, config_name, local_dir, system_dir):
        self.env_key = env_key
        self.config_name = config_name
        self.local_dir = local_dir
        self.system_dir = system_dir

    @property
    def config_name(self):
        return self._config_name

    @config_name.setter
    def config_name(self, value):
        self._config_name = value

    @property
    def env_key(self):
        return self._env_key

    @env_key.setter
    def env_key(self, value):
        self._env_key = value

    @property
    def local_dir(self):
        return self._local_dir

    @local_dir.setter
    def local_dir(self, value):
        self._local_dir = value

    @property
    def system_dir(self):
        return self._system_dir

    @system_dir.setter
    def system_dir(self, value):
        self._system_dir = value

    def get_config(self):
        for config_path in self.config_paths:
            if os.path.exists(config_path):
                provider = get_provider(config_path)
                return Config(provider)

    def get_config_paths(self):
        config_paths = [os.path.join(path, self.config_name)
                        for path in self._get_search_paths() if path is not
                        None]
        config_paths.insert(0, self._get_config_from_env())
        return config_paths

    def _get_config_from_env(self):
        return os.environ.get(self.env_key, None)

    def _get_search_paths(self):
        return [
            self._get_local_dir(),
            self._get_home_dir(),
            self._get_system_dir()
        ]

    def _get_local_dir(self):
        return self.local_dir

    def _get_home_dir(self):
        return os.path.expanduser("~")

    def _get_system_dir(self):
        return self.system_dir

# vim: filetype=python
