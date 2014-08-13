from optparse import make_option

from tests.app0.management.commands.dummy import Command as Command0


class Command(Command0):

    option_list = (make_option('--dummy-one', action='store_true',
                               help="App1 dummy command option"),)

    def handle_noargs(self, **options):
        super(Command, self).handle_noargs(**options)
