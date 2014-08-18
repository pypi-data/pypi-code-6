"""
Django settings for Descartes BI project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
import sys

_file_path = os.path.abspath(os.path.dirname(__file__)).split('/')

BASE_DIR = '/'.join(_file_path[0:-2])

MEDIA_ROOT = os.path.join(BASE_DIR, 'descartes_bi', 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@mff4*!u6*nc5+0pmkvcu#$&n1mq=n=+mb6g%2!ivyj3_m_g-1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    # 3rd party
    'suit',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'compressor',
    'south',

    # Descates BI
    'common',
    'core',
    'datasources',
    'dashboards',
    'widgets',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'descartes_bi.urls'

WSGI_APPLICATION = 'descartes_bi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MEDIA_ROOT, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Custom settings section

from django.utils.translation import ugettext_lazy as _

PROJECT_NAME = 'descartes'
PROJECT_TITLE = _('Descartes BI')

ugettext = lambda s: s

LANGUAGES = (
    ('es', ugettext('Spanish')),
    ('en', ugettext('English')),
)

SITE_ID = 1

STATIC_URL = '/static/'

sys.path.append(os.path.join(BASE_DIR, 'descartes_bi', 'apps'))

STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')

MEDIA_URL = '/site_media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# ===== Configuration options ===============

# --------- Django -------------------
LOGIN_URL = 'common:login_view'
LOGIN_REDIRECT_URL = 'common:home_view'

# ---------- CSS compress ------------
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_ENABLED = False

# Django SUIT

SUIT_CONFIG = {
    'ADMIN_NAME': PROJECT_TITLE,
    'MENU_OPEN_FIRST_CHILD': True,
    'MENU': (
        {'label': _('Auth'), 'icon': 'icon-user', 'app': 'auth'},
        {'label': _('Datasources'), 'icon': 'icon-file', 'app': 'datasources'},
        {'label': _('Dashboards'), 'icon': 'icon-picture', 'app': 'dashboards'},
        {'label': _('Widgets'), 'icon': 'icon-cog', 'app': 'widgets'},
    ),
}

