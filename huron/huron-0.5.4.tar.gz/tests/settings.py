import os, sys

from os.path import abspath, dirname, join
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

ADMINS = (
    ('test@example.com', 'Mr. Test'),
)

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_PATH, 'media'))

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'huron.db'
TEST_DATABASE_NAME = ''

# for forwards compatibility
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'TEST_NAME': TEST_DATABASE_NAME,
    }
}


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'huron.utils',
    'huron.blog',
    'huron.contact_form',
    'huron.menus_manager',
    'huron.pages',
    'huron.settings',
    'huron.simple_medias_manager',
    'huron.simple_news',
    'huron.slider',
]

ROOT_URLCONF = 'tests.urls'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'verysecret'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'py.warnings': {
            'level': 'ERROR',# change to WARNING to show DeprecationWarnings, etc.
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# to make sure timezones are handled correctly in Django>=1.4
USE_TZ = True
