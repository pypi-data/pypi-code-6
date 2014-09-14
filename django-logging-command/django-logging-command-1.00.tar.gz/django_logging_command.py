import logging
from optparse import make_option


class LoggingCommandMixin(object):
    """
    Mixin to be used BEFORE inheriting from a base command.

    For example:
        class Command(LoggingCommandMixin, base.NoArgsCommand):
    """

    def __init__(self):
        # noinspection PyUnresolvedReferences
        self.option_list += (
            make_option('-s', action='store_true', dest='silentmode',
                        default=False, help='Run in silent mode'),
            make_option('--extrasilent', action='store_true',
                        dest='extrasilent', default=False,
                        help='Run in silent mode'),
            make_option('--debug', action='store_true',
                        dest='debugmode', default=False,
                        help='Debug mode (overrides silent mode)'),
        )
        super(LoggingCommandMixin, self).__init__()

    def handle(self, *args, **options):
        if options['debugmode']:
            logging.getLogger('').setLevel(logging.DEBUG)
        elif options['silentmode']:
            logging.getLogger('').setLevel(logging.WARNING)
        elif options['extrasilent']:
            logging.getLogger('').setLevel(logging.CRITICAL)
        else:
            logging.getLogger('').setLevel(logging.INFO)
        super(LoggingCommandMixin, self).handle(*args, **options)