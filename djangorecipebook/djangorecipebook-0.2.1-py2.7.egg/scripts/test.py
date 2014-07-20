"""
Recipe generating a test script
"""

import sys


def main(settings_module, *apps):
    from django.core import management
    settings = []
    for arg in sys.argv:
        if arg.startswith('--settings='):
            break
    else:
        settings = ['--settings=%s' % settings_module]
    management.execute_from_command_line(['manage.py', 'test'] + \
                                         sys.argv[1:] + settings + \
                                         list(apps))
