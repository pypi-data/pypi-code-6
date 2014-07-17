import os

import warnings
import exceptions

from mayan.settings.base import *


warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning)

SECRET_KEY='2kj23k4j324'

DEBUG = True
ALLOWED_HOSTS = ['*']
#TEMPLATE_DEBUG = DEBUG

#CONVERTER_GRAPHICS_BACKEND = u'converter.backends.python'
#CONVERTER_GRAPHICS_BACKEND = u'converter.backends.imagemagick'
#CONVERTER_GRAPHICS_BACKEND = u'converter.backends.graphicsmagick'
#CONVERTER_GM_SETTINGS = u'-limit files 1 -limit memory 1GB -limit map 2GB -density 200'

#GROUPING_SHOW_EMPTY_GROUPS = False
#DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD = True
#DOCUMENT_AUTOMATIC_OCR = True
#DOCUMENTS_ZOOM_PERCENT_STEP = 25
#DOCUMENTS_ZOOM_MAX_LEVEL = 200
#DOCUMENTS_ZOOM_MIN_LEVEL = 25
#DOCUMENTS_DISPLAY_SIZE = '2000'
#DOCUMENTS_TRANFORMATION_PREVIEW_SIZE = '640x480'

#OCR_TESSERACT_LANGUAGE = 'rus'
#OCR_TESSERACT_LANGUAGE = 'spa'
#OCR_REPLICATION_DELAY = 20
#OCR_NODE_CONCURRENT_EXECUTION = 1
#OCR_QUEUE_PROCESSING_INTERVAL = 3  # In seconds

#STORAGE_FILESTORAGE_LOCATION = u'/home/rosarior/development/mayan/mayan/document_storage'
#WEB_THEME_THEME = u'djime-cerulean'
# Change to xsendfile for apache if x-sendfile is enabled
#SENDFILE_BACKEND = 'sendfile.backends.sendfile'
#SEARCH_LIMIT = 50

if 0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mayan_development',     # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': '584853069',                  # Not used with sqlite3.
            #'HOST': '192.168.1.133',                      # Set to empty string for localhost. Not used with sqlite3.
            #'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'HOST': '192.168.10.20',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
if 0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'ods',     # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': '584853069',                  # Not used with sqlite3.
            #'HOST': '192.168.1.133',                      # Set to empty string for localhost. Not used with sqlite3.
            'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

if 0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mayan',     # Or path to database file if using sqlite3.
            'USER': 'mayan',                      # Not used with sqlite3.
            'PASSWORD': 'yanma',                  # Not used with sqlite3.
            #'HOST': '192.168.1.133',                      # Set to empty string for localhost. Not used with sqlite3.
            'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

#ENABLE_TRANSLATION_SUGGESTIONS = False
#WEB_THEME_VERBOSE_LOGIN = False
#MAIN_SIDE_BAR_SEARCH = True

#MAIN_DISABLE_HOME_VIEW = True

#amro, bec, bec-green, blue, default, djime-cerulean, drastic-dark, kathleene, olive, orange, red, reidb-greenish and warehouse
#WEB_THEME_THEME = 'default'
#MAIN_DISABLE_ICONS = True

#TEMPLATE_STRING_IF_INVALID = 'ERROR'
#AUTHENTICATION_BACKENDS = ('common.auth.email_auth_backend.EmailAuthBackend',)
#COMMON_LOGIN_METHOD = 'email'

#COMPRESS_ENABLED = True
#COMPRESS_PARSER = 'compressor.parser.HtmlParser'
#COMPRESS_PARSER = 'compressor.parser.BeautifulSoupParser'
#COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.SlimItFilter']
#COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
#COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
        },
        'intermediate': {
            'format': '%(name)s <%(process)d> [%(levelname)s] "%(funcName)s() %(message)s"'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        #'mail_admins': {
        #    'level': 'ERROR',
        #    'class': 'django.utils.log.AdminEmailHandler'
        #},
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'intermediate'
        }
    },
    'loggers': {
        #'django.request': {
        #    'handlers': ['console'],
        #    'level': 'DEBUG',
        #    #'propagate': True,
        #},
        #'django': {
        #    'handlers':['console'],
        #    'propagate': True,
        #    'level':'DEBUG',
        #},
        #'converter.office_converter': {
        #    'handlers':['console'],
        #    #'propagate': True,
        #    'level':'DEBUG',
        #    #'level':'INFO',
        #},
        'django.template': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'ocr': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'dynamic_search': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'documents': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'converter': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'scheduler': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'signaler': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'dynamic_search': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'checkouts': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'history': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'apscheduler.scheduler': {
            'handlers':['console'],
            'propagate': True,
            'level':'ERROR',
        },
        'job_processor': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'clustering': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'common': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'backups': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        #'app_registry': {
        #    'handlers':['console'],
        #    'propagate': True,
        #    'level':'DEBUG',
        #},
    }
}


WEB_THEME_THEME = 'activo'

#COMPRESS_ENABLED=True

#COMMON_ALLOW_ANONYMOUS_ACCESS=True

#SIGNATURES_GPG_HOME = '/bin/asd'

#COMMON_LOGIN_METHOD = 'email'
#AUTHENTICATION_BACKENDS = ('common.auth.email_auth_backend.EmailAuthBackend',)


#DOCUMENT_INDEXING_FILESYSTEM_FILESERVING_PATH='/tmp/mayan/'
#DOCUMENT_INDEXING_FILESYSTEM_FILESERVING_ENABLE = True


#WEB_THEME_THEME = 'default'
#CSS theme to apply, options are: ``amro``, ``bec``, ``bec-green``, ``blue``,
#``default``, ``djime-cerulean``, ``drastic-dark``, ``kathleene``, ``olive``,
#``orange``, ``red``, ``reidb-greenish`` and ``warehouse``.

#WEB_THEME_VERBOSE_LOGIN
#WEB_THEME_VERBOSE_LOGIN=False

#MAIN_DISABLE_HOME_VIEW=True
#MAIN_DISABLE_ICONS=True
#MAIN_SIDE_BAR_SEARCH = True


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'roberto.rosario.gonzalez@gmail.com'
EMAIL_HOST_PASSWORD = 'sbsp040324'
EMAIL_PORT = 587

#SOURCES_EMAIL_PROCESSING_INTERVAL=55555

#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr'
#    },
#}
#SEARCH_INDEX_UPDATE_INTERVAL = 5
#DEBUG_ON_EXCEPTION = True
