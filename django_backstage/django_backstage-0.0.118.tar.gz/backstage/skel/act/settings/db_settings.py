import os
from . import settings.VENUE_NAME

DBENGINE = 'django.db.backends.postgresql_psycopg2'
DBHOST = '127.0.0.1'
DBPORT = 5433
DBUSER = ''
DBPASS = ''
DBNAME = 'backstage_%s_%s' % (settings.VENUE_NAME, river_acts_mfgis'

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
