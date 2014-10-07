"""
Recipe generating a management script
"""

import sys


def manage_main(settings_module, command, *args):
    from django.core import management
    settings = []
    for arg in sys.argv:
        if arg.startswith('--settings='):
            break
    else:
        settings = ['--settings=%s' % settings_module]

    if command:
        command = [command]
    else:
        try:
            command = [sys.argv.pop(1)]
        except IndexError:
            raise ValueError('No django command found. A django command is '
                             'required when calling manage.py.')

    # the arguments need to be inserted in sys.argv as subsequent packages
    # (e.g. nose via django_nose) fetch them directly from it
    sys.argv[1:1] = args
    management.execute_from_command_line(['manage.py'] + command +
                                         settings + sys.argv[1:])


def main(settings_module, *args):
    manage_main(settings_module, None, *args)
