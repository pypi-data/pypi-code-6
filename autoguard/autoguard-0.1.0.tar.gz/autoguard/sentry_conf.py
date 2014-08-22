# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polyconseil SAS.
# This code is distributed under the two-clause BSD License.

from __future__ import unicode_literals
import base64
import logging
import os
import os.path
import urlparse
import warnings

from getconf import ConfigGetter


def url_value_converter(value):
    value_to_convert = {
        'True': True,
        'False': False,
    }

    return value_to_convert.get(value, value)


def database_from_url(url):
    db_shortcuts = {
        'postgresql': 'django.db.backends.postgresql_psycopg2',
        'postgres': 'django.db.backends.postgresql_psycopg2',
        'sqlite': 'django.db.backends.sqlite3',
    }

    parsed = urlparse.urlparse(url)
    parsed_qs = urlparse.parse_qs(parsed.query)
    if any([len(value) > 1 for value in parsed_qs.values()]):
        warnings.warn("settings: django.db_url: one argument is set more than once, only use first one.")

    return {
        'ENGINE': db_shortcuts.get(parsed.scheme, parsed.scheme),
        'NAME': parsed.path[1:],
        'USER': parsed.username,
        'PASSWORD': parsed.password,
        'HOST': parsed.hostname,
        'PORT': parsed.port,
        'OPTIONS': {
            key: url_value_converter(value[0])
            for key, value in parsed_qs.items()
        }
    }


def mail_from_url(url):
    backend_shortcuts = {
        'smtp': 'django.core.mail.backends.smtp.EmailBackend',
        'console': 'django.core.mail.backends.console.EmailBackend',
    }

    parsed = urlparse.urlparse(url)
    config = {
        'backend': backend_shortcuts.get(parsed.scheme, parsed.scheme),
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
        'use_tls': False,
        'sender': "no-reply@{}".format(parsed.hostname if parsed.hostname else 'localhost')
    }
    config.update({
        key: url_value_converter(value[0])
        for key, value in urlparse.parse_qs(parsed.query).items()
    })
    return config


def cache_from_url(url):
    backend_shortcuts = {
        'db': 'django.core.cache.backends.db.DatabaseCache',
        'dummy': 'django.core.cache.backends.dummy.DummyCache',
        'file': 'django.core.cache.backends.filebased.FileBasedCache',
        'mem': 'django.core.cache.backends.locmem.LocMemCache',
        'memcached': 'django.core.cache.backends.memcached.MemcachedCache'
    }

    parsed = urlparse.urlparse(url)
    return {
        'BACKEND': backend_shortcuts.get(parsed.scheme, parsed.scheme),
        'LOCATION': parsed.netloc,
    }


def sentry_buffer_from_url(url):
    backend_shortcuts = {
        'base': 'sentry.buffer.base.Buffer',
        'redis': 'sentry.buffer.redis.RedisBuffer',
    }

    parsed = urlparse.urlparse(url)
    config = {
        'backend': backend_shortcuts.get(parsed.scheme, parsed.scheme),
        'options': {},
    }

    if config['backend'] == backend_shortcuts['redis']:
        config['options'] = {
            'hosts': {
                0: {
                    'host': parsed.hostname,
                    'port': parsed.port,
                }
            }
        }

    return config

PROJECT_NAME = 'autoguard'  # Name of the project (e.g GitHub repository)
CONFIG = ConfigGetter(
    PROJECT_NAME,
    '/etc/%s/settings.ini' % PROJECT_NAME,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'local_settings.ini')),
)

# Django Configuration
# ====================
DEBUG = CONFIG.getbool('dev.debug', False, doc="Enable debug mode.")
TIME_ZONE = CONFIG.get('django.time_zone', default='Europe/Paris')
SECRET_KEY = CONFIG.get('django.secret_key', base64.b64encode(os.urandom(40)))

DATABASES = {
    'default': database_from_url(CONFIG.get('django.db_uri', 'sqlite:///sentry.sqlite'))
}

CACHES = {
    'default': cache_from_url(CONFIG.get('django.cache_uri', 'mem://'))
}

_parsed_email_url = mail_from_url(CONFIG.get('django.mail_uri', 'console://?sender=no-reply@localhost'))
EMAIL_BACKEND = _parsed_email_url['backend']
EMAIL_HOST = _parsed_email_url['host']
EMAIL_PORT = _parsed_email_url['port']
EMAIL_USER = _parsed_email_url['user']
EMAIL_PASSWORD = _parsed_email_url['password']
EMAIL_USE_TLS = _parsed_email_url['use_tls']
SERVER_EMAIL = _parsed_email_url['sender']

BROKER_URL = CONFIG.get('django.queue_broker_url', default=None)
CELERY_ALWAYS_EAGER = BROKER_URL is None

_site_parsed_url = urlparse.urlparse(CONFIG.get('django.site_url', 'http://localhost:9000'))
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", _site_parsed_url.hostname]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Sentry Configuration
# ====================
SENTRY_URL_PREFIX = _site_parsed_url.geturl()

SENTRY_WEB_HOST = CONFIG.get('host', '127.0.0.1')
SENTRY_WEB_PORT = CONFIG.getint('port', 9000)
SENTRY_WEB_OPTIONS = {
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    'workers': CONFIG.getint('sentry.workers', 5),
}

_parsed_sentry_buffer = sentry_buffer_from_url(CONFIG.get('sentry.buffer_uri', 'base://'))
SENTRY_BUFFER = _parsed_sentry_buffer['backend']
SENTRY_BUFFER_OPTIONS = _parsed_sentry_buffer['options']

SENTRY_PUBLIC = CONFIG.getbool('sentry.public', default=False, doc="Whether not authenticated user can read data.")
SENTRY_SAMPLE_DATA = CONFIG.getbool('sentry.sample_data', default=True, doc="Use data sampling.")

SENTRY_ALLOW_REGISTRATION = False  # no auto-registration
SOCIAL_AUTH_CREATE_USERS = False  # no auto-registration

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
