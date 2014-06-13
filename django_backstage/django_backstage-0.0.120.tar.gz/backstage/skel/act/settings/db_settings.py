import os
from .settings import VENUE_NAME, ACT_NAME

DBENGINE = 'django.db.backends.postgresql_psycopg2'
DBHOST = '127.0.0.1'
DBPORT = 5433
DBUSER = ''
DBPASS = ''
DBNAME = 'backstage_%s_%s' % (VENUE_NAME, ACT_NAME)

DATABASES = {}
DATABASES['default'] = {
    'NAME': DBNAME,
    'ENGINE': DBENGINE,
    'HOST': DBHOST,
    'PORT': DBPORT,
    'USER': DBUSER,
    'PASSWORD': DBPASS
}

DEFAULT_DB_ALIAS='default'
DEFAULT_DB = DATABASES['default']
