# -*- coding:utf-8 -*-
from django.conf import settings

FBAUTH_REDIRECT_URL = unicode(getattr(settings, 'FBAUTH_REDIRECT_URL', '{0}'))
FBAUTH_FACEBOOK_APP_ID = getattr(settings, 'FBAUTH_FACEBOOK_APP_ID', '')
FBAUTH_FACEBOOK_LOCALE = getattr(settings, 'FBAUTH_FACEBOOK_LOCALE', 'en_US')
