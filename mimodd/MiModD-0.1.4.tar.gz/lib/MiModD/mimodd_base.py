# from argparse import Action, SUPPRESS, _sys

class Version (tuple):
    def __str__ (self):
        return '.'.join(str(d) for d in self)

# VERSION
version = Version((0, 0, 1))

def catch_sigterm (signum, frame):
    """Define package-wide behavior on SIGTERM."""

    raise RuntimeError ('Execution stopped by system.')

#class VersiontoStdoutAction(Action):
#    def __init__(self,
#                 option_strings,
#                 version=None,
#                 dest=SUPPRESS,
#                 default=SUPPRESS,
#                 help="show program's version number and exit"):
#        super(VersiontoStdoutAction, self).__init__(
#            option_strings=option_strings,
#            dest=dest,
#            default=default,
#            nargs=0,
#            help=help)
#        self.version = version
#
#    def __call__(self, parser, namespace, values, option_string=None):
#        version = self.version
#        if version is None:
#            version = parser.version
#        formatter = parser._get_formatter()
#        formatter.add_text(version)
#        parser._print_message(formatter.format_help(), _sys.stdout)
#        parser.exit()
