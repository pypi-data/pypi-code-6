#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of holmesalf.
# https://github.com/holmes-app/holmes-alf

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Pablo Aguiar scorphus@gmail.com

from holmesalf.version import __version__


class BaseAuthNZWrapper(object):
    """This class gathers authentication and authorization
    for some of the services used by Holmes"""
    def __init__(self, config):
        raise NotImplementedError()

    @property
    def sync_client(self):
        """Synchronous client"""
        raise NotImplementedError()

    @property
    def async_client(self):
        """Asynchronous client"""
        raise NotImplementedError()
