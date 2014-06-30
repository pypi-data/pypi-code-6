from unipath import Path
import json
import os


BASE = Path(__file__).absolute().ancestor(2)

try:
    with open(BASE.child('secrets.json')) as handle:
        SECRETS = json.load(handle)
except IOError:
    SECRETS = {}

SECRET_KEY = SECRETS.get('secret_key', '{{ secret_key }}')
PRODUCTION = SECRETS.get('production', False)

DEBUG = not PRODUCTION
TEMPLATE_DEBUG = not PRODUCTION

ALLOWED_HOSTS = [SECRETS.get('allowed_hosts')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ROOT_URLCONF = '{{ project_name }}.urls'
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

if not SECRETS.get('engine') or SECRETS.get('engine') == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': SECRETS.get('db_name', os.path.join(BASE, 'db.sqlite3')),
        }
    }
elif SECRETS.get('engine') == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': SECRETS.get('db_name', 'dbname'),
            'USER': SECRETS.get('db_user', 'root'),
            'PASSWORD': SECRETS.get('db_password', 'password'),
            'HOST': SECRETS.get('db_host', '127.0.0.1'),
        }
    }

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = "SHORT_DATE_FORMAT"

TEMPLATE_DIRS = [BASE.child('templates')]
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE.child('static')]
STATIC_ROOT = BASE.child('static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE.child('media')
