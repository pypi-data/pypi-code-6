#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of holmesalf.
# https://github.com/holmes-app/holmes-alf

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Pablo Aguiar scorphus@gmail.com

from holmesalf import BaseAuthNZWrapper

from alf.client import Client as AlfSyncClient
from tornadoalf.client import Client as AlfAsyncClient


class AlfAuthNZWrapper(BaseAuthNZWrapper):
    """This class gathers authentication and authorization
    for some of the services used by Holmes"""
    def __init__(self, config):
        self.config = config
        self._sync_client = None
        self._async_client = None

    @property
    def sync_client(self):
        """Synchronous OAuth 2.0 Bearer client"""
        if not self._sync_client:
            self._sync_client = AlfSyncClient(
                token_endpoint=self.config.get('OAUTH_TOKEN_ENDPOINT'),
                client_id=self.config.get('OAUTH_CLIENT_ID'),
                client_secret=self.config.get('OAUTH_CLIENT_SECRET')
            )
        return self._sync_client

    @property
    def async_client(self):
        """Asynchronous OAuth 2.0 Bearer client"""
        if not self._async_client:
            self._async_client = AlfAsyncClient(
                token_endpoint=self.config.get('OAUTH_TOKEN_ENDPOINT'),
                client_id=self.config.get('OAUTH_CLIENT_ID'),
                client_secret=self.config.get('OAUTH_CLIENT_SECRET')
            )
        return self._async_client
