######################
# Standard Libraries #
######################
from __future__ import absolute_import
from pprint     import pprint
from functools  import wraps

import os

#########################
# Third Party Libraries #
#########################

### The boto library
import boto
import boto.ec2

from boto.ec2 import get_region


### for the application class
import krux.cli

from krux.constants     import DEFAULT_LOG_LEVEL
from krux.logging       import get_logger, LEVELS
from krux.stats         import get_stats
from krux.cli           import get_parser, get_group


### Constants
ACCESS_KEY      = 'AWS_ACCESS_KEY_ID'
SECRET_KEY      = 'AWS_SECRET_ACCESS_KEY'
NAME            = 'krux-boto'
DEFAULT_REGION  = 'us-east-1'

### Designed to be called from krux.cli, or programs inheriting from it
def add_boto_cli_arguments(parser):

    group = get_group(parser, 'boto')

    group.add_argument(
        '--boto-log-level',
        default = DEFAULT_LOG_LEVEL,
        choices = LEVELS.keys(),
        help    = 'Verbosity of boto logging. (default: %(default)s)'
    )

    group.add_argument(
        '--boto-access-key',
        default = os.environ.get(ACCESS_KEY),
        help    = 'AWS Access Key to use. Defaults to ENV[%s]' % ACCESS_KEY,
    )

    group.add_argument(
        '--boto-secret-key',
        default = os.environ.get(SECRET_KEY),
        help    = 'AWS Secret Key to use. Defaults to ENV[%s]' % SECRET_KEY,
    )

    group.add_argument(
        '--boto-region',
        default = DEFAULT_REGION,
        choices = [r.name for r in boto.ec2.regions()],
        help    = 'EC2 Region to connect to. (default: %(default)s)',
    )


class Boto(object):
    def __init__(self, logger = None, stats = None, parser = None):


        ### Because we're wrapping boto directly, use ___ as a prefix for
        ### all our variables, so we don't clash with anything public
        self.___name   = NAME
        self.___logger = logger or get_logger(self.___name)
        self.___stats  = stats  or get_stats( prefix      = self.___name)
        self.___parser = parser or get_parser(description = self.___name)

        ### in case we got some of the information via the CLI
        self.___args    = self.___parser.parse_args()

        ### this has to be 'public', so callers can use it. It's unfortunately
        ### near impossible to transparently wrap this, because the boto.config
        ### is initialized before we get here, and all the classes do a look up
        ### at compile time. So overriding doesn't help.
        ### Wrapping doesn't work cleanly, because we 1) would have to wrap
        ### everything, including future features we can't know about yet, as
        ### well as 2) poke into the guts of the implementation classes to figure
        ### out connection strings etc. It's quite cumbersome.
        ### So for now, we just store the region that was asked for, and let the
        ### caller use it. See the sample app for a howto.
        self.cli_region = self.___args.boto_region

        ### if these are set, make sure we set the environment again
        ### as well; that way the underlying boto calls will just DTRT
        ### without the need to wrap all the functions.
        map = {
            'boto_access_key': ACCESS_KEY,
            'boto_secret_key': SECRET_KEY,
        }

        for name, env_var in map.iteritems():
            val = getattr( self.___args, name, None )

            if val is not None:

                ### this way we can tell what credentials are being used,
                ### without dumping the whole secret into the logs
                pp_val = val[0:3] + '[...]' + val[-3:] if len(val) else '<empty>'
                self.___logger.debug(
                    'Setting boto credential %s to %s', env_var, pp_val
                )

                os.environ[ env_var ] = val

            ### If at this point the environment variable is NOT set,
            ### you didn't set it, and we didn't set it. At which point
            ### boto will go off spelunking for .boto files or other
            ### settings. Best be clear about this. Using 'if not' because
            ### if you set it like this:
            ### $ FOO= ./myprog.py
            ### It'll return an empty string, and we'd not catch it.
            if not os.environ.get( env_var, None ):
                self.___logger.info(
                    'Boto environment credential %s NOT explicitly set ' +
                    '-- boto will look for a .boto file somewhere', env_var
                )

        ### This sets the log level for the underlying boto library
        get_logger('boto').setLevel( LEVELS[ self.___args.boto_log_level ] )

        ### access it via the object
        self.___boto = boto

    def __getattr__(self, attr):
        """Proxies calls to ``boto.*`` methods."""

        ### This way, we don't have to write: rv = Boto().boto.some_call
        ### But can just write: rv = Boto().some_call
        ### This also gives us hooks for future logging/timers/etc and
        ### extended wrapping of things the attributes return if we so
        ### choose.
        self.___logger.debug('Calling wrapped boto attribute: %s', attr)

        attr = getattr(self.___boto, attr)

        if callable(attr):
            self.___logger.debug("Boto attribute '%s' is callable", attr)

            @wraps(attr)
            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)
            return wrapper

        return attr


class Application(krux.cli.Application):

    def __init__(self, name = NAME):
        ### Call to the superclass to bootstrap.
        super(Application, self).__init__(name = name)

        self.boto = Boto(
            parser = self.parser,
            logger = self.logger,
            stats  = self.stats,
        )

    def add_cli_arguments(self, parser):

        ### add the arguments for boto
        add_boto_cli_arguments(parser)


def main():
    app    = Application()
    region = boto.ec2.get_region(app.boto.cli_region)
    ec2    = app.boto.connect_ec2(region = region)

    app.logger.warn('Connected to region: %s', region.name)
    for r in ec2.get_all_regions():
        app.logger.warn('Region: %s', r.name)


### Run the application stand alone
if __name__ == '__main__':
    main()
