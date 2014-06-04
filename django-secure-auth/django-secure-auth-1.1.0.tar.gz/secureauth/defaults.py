# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.conf import settings


def get_settings(key, default):
    return getattr(settings, key, default)


SMS_FORCE = get_settings('AUTH_SMS_FORCE', False)
SMS_BACKEND = get_settings('AUTH_SMS_BACKEND', 'Twilio')
SMS_BACKEND_AUTH = get_settings('AUTH_SMS_BACKEND_AUTH', [
    'ACc73704107c6a5426b2157e279c485d32', 'a2949613dc22aa3df58ea813a6e0747f'
])
SMS_FROM = get_settings('AUTH_SMS_FROM', '+12242315966')
SMS_MESSAGE = get_settings('AUTH_SMS_MESSAGE', _('Your code is: %s'))
SMS_CODE_LEN = get_settings('AUTH_SMS_CODE_LEN', 4)
SMS_AGE = get_settings('AUTH_SMS_AGE', 60)
SMS_ASCII = get_settings('AUTH_SMS_ASCII', False)
CODE_RANGES = get_settings('AUTH_CODE_RANGES', 20)
CODE_LEN = get_settings('AUTH_CODE_LEN', 6)
TOTP_NAME = get_settings('AUTH_TOTP_NAME', "%(username)s@%(domain)s")

# Available: code, token, phone, question
DEFAULT_AUTH_TYPE = get_settings('AUTH_DEFAULT_TYPE', 'phone')

# Notification when user is authenticated on site
SMS_NOTIFICATION_SUBJECT = get_settings(
    'AUTH_SMS_NOTIFICATION_SUBJECT', _('Auth activity'))
CODES_SUBJECT = get_settings(
    'AUTH_CODES_SUBJECT', _('Your security codes'))
SMS_NOTIFICATION_MESSAGE = get_settings(
    'AUTH_SMS_NOTIFICATION_MESSAGE',
    _("Authorization was made. If it's not you, then contact with us."))

USE_CELERY = get_settings(
    'AUTH_USE_CELERY', 'djcelery' in settings.INSTALLED_APPS)

ACTIVITY_PER_PAGE = get_settings('AUTH_ACTIVITY_PER_PAGE', 8)

METHODS_ENABLED = get_settings('AUTH_METHODS_ENABLED', (
    'token',
    'phone',
    'question',
    'code',
    'activity',
    'notification',
    'logging',
))

CHECK_ATTEMPT = get_settings('AUTH_CHECK_ATTEMPT', True)
LOGIN_ATTEMPT = get_settings('AUTH_LOGIN_ATTEMPT', 5)
BAN_TIME = get_settings('AUTH_LOGIN_ATTEMPT_BAN_TIME', 3600)

CAPTCHA_ENABLED = get_settings('AUTH_CAPTCHA_ENABLED', True)
CAPTCHA_ATTEMPT = get_settings('AUTH_CAPTCHA_ATTEMPTS', 1)

CHECK_PASSWORD = get_settings('AUTH_CHECK_PASSWORD', True)
