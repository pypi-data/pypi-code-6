# -*- coding:utf-8 -*-
from django.apps import AppConfig

from . import strings


class FBAuthConfig(AppConfig):
    name = 'fbauth'
    verbose_name = strings.APP_VERBOSE_NAME
