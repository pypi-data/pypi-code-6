# -*- coding: utf-8 -*-
from .default import *

TORNADO_PORT = 8885
BASE_URL = 'http://localhost:%s' % TORNADO_PORT

DATABASE = {'default': {'host': 'localhost',
                        'port': 27017,
                        'db': 'pyrocumulus-functestpy34'}}
