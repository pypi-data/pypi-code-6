# -*- coding: utf-8 -*-
from .default import *

TORNADO_PORT = 8887
BASE_URL = 'http://localhost:%s' % TORNADO_PORT

DATABASE = {'default': {'host': 'localhost',
                        'port': 27017,
                        'db': 'pyrocumulus-functestpy33'}}
