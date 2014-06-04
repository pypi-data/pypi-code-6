# -*- coding: utf-8 -*-

import os

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'concordbay',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static', 'files')

YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20131123T222315Z.a0b80d29c8a8898d.8cecd7d9e36764fe56b95c06e1918041fd360dc5'
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_WSGI_AUTO_RELOAD = True


DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'EXCLUDE_URLS': ('/admin',),
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
}

INTERNAL_IPS = ('127.0.0.12',)

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'


_ = lambda s: s

LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, '../locale'),
)

#AUTH_CHECK_PASSWORD = False
