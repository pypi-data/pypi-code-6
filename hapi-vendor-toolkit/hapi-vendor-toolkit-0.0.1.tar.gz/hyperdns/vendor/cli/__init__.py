"""Multi-Vendor Command Line Interface

Note: this uses 'click' - http://click.pocoo.org, please see the notes
relevant to this structure.  I had previously tried docopt, but that didn't
quite get what I wanted - then I tried click and it had a similar problem,
however, I do *not* want to roll my own and went with click.

The problem was the need to interleave the 'config' command with the vendor
scoped commands.  I use 'dns' as the command name and would like the following
four commands to work:

    dns
    dns add <vendor-id>
    dns new <vendor-id> <path-to-new-repo>
    dns info
    dns config
    dns <vendor> <standard set of commands>

where dns, by itself, dumps a useful help screen that tells you more than
you ever wanted to know.  'dns info' can provide more detailed information
and  'dns config' takes you through an interactive configuration analysis
and setup.
use `dns add` to add vendors from PyPI and `dns new` to create new vendor
repositories.

Summary of contents:

 - first section implements the driver_registry, and discovers all currently
   available drivers installed within your path.  This will translate into
   commands available via `dns <vkey>`

 - :class:VendorUtilities implements functions against a driver, and prints
   the results to system out.
   
 - :class:VendorShell implements a :package:cmd.Cmd based interactive shell
   accessible via `dns <vkey> shell`.  This is an adapter for
   :class:VendorUtilities and handles the parsing of the interactive command
   line.
   
 - :class:VendorCommands implements a suite of :package:click based commands
   which support `dns <vkey> <command>` usage.  This is an adapter for
   :class:VendorUtilities and handles the coupling with :package:click API.
   
   Sub-command groups are implemented as subclasses.  For example, the upload
   facility is implemented in :class:VendorCommands.UploadCommands, which further
   breaks down into uploading a BIND9 Zonefile or a HAPI DNS JSON record.
   
 - :class:VendorCLI provides a top level :class:click.MultiCommand supporting
   the top level commands like new, add, info, and config.
   
 - top level functions which implement the commands themselves.

"""

import os,sys

# this stuff needs to come from setup.py
def purepath(rp):
    return os.path.join(os.path.dirname(__file__),rp)
PROGNAME=os.path.basename(sys.argv[0])
import click

class BaseCommand(click.MultiCommand):
    def __init__(self,dclass):
        click.MultiCommand.__init__(self)
        self.dclass=dclass

    def get_command(self,ctx,name):
        try:
            l=self.list_commands(ctx)
            if name not in l:
                click.echo("Perhaps you are missing one of these subcommands:%s " % l)
                return None
            return getattr(self,name)
        except AttributeError:
            return None

    def _driver(self,ctx,login=False):
        """Return the appropriate driver
        """
        settings=ctx['config']['vendors'].get(self.vkey,None)
        if settings==None:
            raise Exception('Can not obtain driver without credentials')
        return self.dclass(settings,immediateLogin=login)

# this line is used by setup.py to define the 'dns' entry_point
from .main import cli as main
from .shell import VendorShell


