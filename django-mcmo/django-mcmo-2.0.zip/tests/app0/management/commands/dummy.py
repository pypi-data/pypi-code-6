"""
This is the base command, from which all other are supposed to derive
"""

from optparse import make_option

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):

    option_list = (make_option('--dummy-zero', action='store_true',
                               help="App0 dummy command option"),)

    def handle_noargs(self, **options):
        pass
