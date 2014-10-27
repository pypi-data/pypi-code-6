"""
django-bootstrap3-wysihtml5x - Simple Django app that allows using the rich text editor Wysihtml5 in text fields.
"""

default_app_config = 'bootstrap3_wysihtml5x.apps.Bootstrap3Wysihtml5xConfig'

VERSION = (1, 0, 0, 'b', 1) # following PEP 386

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3] != 'f':
        version = '%s%s%s' % (version, VERSION[3], VERSION[4])
    return version
