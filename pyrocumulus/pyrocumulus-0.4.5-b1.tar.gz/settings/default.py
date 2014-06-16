#-*- coding: utf-8 -*-

import os

# Basic server config
TORNADO_PORT = 8888
BASE_URL = 'http://localhost:%s' % TORNADO_PORT
STATIC_URL = '/static/'
CORS_ORIGINS = '*'
DEBUG = True

# database settings
DATABASE = {'default': {'host': 'localhost',
                        'port': 27017,
                        'db': 'pyrocumulus-dev'}}


# directories containing static files
# static dir for functional tests
basedir = os.path.abspath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../'))
test_dir = os.path.join(basedir, 'functional_tests')
test_data_dir = os.path.join(test_dir, 'testdata/')

STATIC_DIRS = [test_data_dir]

# directories containing templates
TEMPLATE_DIRS = [test_data_dir]

# application to be served by tornado
APPLICATIONS = []
