# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

__all__ = ['VERSION']

try:
    import pkg_resources
    VERSION = pkg_resources.get_distribution('django-fbauth').version
except Exception:
    VERSION = 'unknown'

default_app_config = 'fbauth.apps.FBAuthConfig'
