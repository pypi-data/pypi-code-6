"""strikepackage

strikepackage thinks your mom is a classy lady.

Usage:
  strikepackage deploy <xenserver_url> [--conf <config_file>]
  strikepackage mkconfig
  strikepackage (-h | --help)
  strikepackage (-v | --version)

Examples:
    * Run strikepackage against XenServer API:
    strikepackage deploy https://myxenserver.domain.local

    * Create default dirs and examples in ~/.strikepackage:
    strikepackage mkconfig

Options:
  -h --help      Show this screen.
  -v --version   Show version.
  --conf <file>  Specify alternate configuration file

"""

__version__ = '0.5.3'

import sys

from docopt import docopt

from .xenserver import get_session
from .utils import get_params
from .config import load_args, mkconfig
from .engage import engage


def main():
    session = None
    try:
        args = docopt(__doc__, version=__version__)
        if args['mkconfig']:
            mkconfig()
            print "PROTIP: Check out ~/.strikepackage"
            sys.exit()
        elif args['deploy']:
            if '--conf' in args:
                config = load_args(args['--conf'])
            else:
                config = load_args()
            session = get_session(args['<xenserver_url>'])
            params = get_params(session, config)
            engage(config, session, params)
            sys.exit()
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print "\nOkay, bye.\n"
        sys.exit(130)
    finally:
        if session is not None:
            session.xenapi.session.logout()
