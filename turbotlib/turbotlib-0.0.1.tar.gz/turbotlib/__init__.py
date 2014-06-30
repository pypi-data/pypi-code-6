from __future__ import print_function

import os
import sys


# We are running in production if MORPH_URL is set in the environment.
in_production = bool(os.getenv('MORPH_URL'))

if in_production:
    data_dir = '/data'
else:
    data_dir = 'data'


def log(message):
    print(message, file=sys.stderr)
