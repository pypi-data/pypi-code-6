"""
Recipe generating a management script
"""

import sys


def main(settings_module):
    # called on script execution
    from django.core import management
    settings = []
    for arg in sys.argv:
        if arg.startswith('--settings='):
            break
    else:
        settings = ['--settings=%s' % settings_module]
    management.execute_from_command_line(sys.argv + settings)
