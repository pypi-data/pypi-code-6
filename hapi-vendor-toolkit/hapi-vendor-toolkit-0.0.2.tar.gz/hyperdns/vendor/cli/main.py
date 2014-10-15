import click,os,json,logging,logging.config
import subprocess
from hyperdns.vendor.cli import PROGNAME
from hyperdns.vendor.core import (
    import_driver,
    getAvailableVendorKeyNameTuples,
    getAvailableVendorKeys
)
from .new_vendor import new_vendor
from .config import config_doctor,_run_config_doctor
from .vendors import VendorCommands

@click.argument('vkey')
@click.pass_obj
def add_vendor(ctx,vkey):
    """Add a vendor library to the current environment if we can locate it on PyPI
    """
    dclass=import_driver(vkey)
    if dclass!=None:
        click.echo("%s is already installed" % vkey)
    else:
        result=subprocess.call(["pip","install","hapi-vendor-%s" % vkey])
        if result==0:
            result=subprocess.call(["dns",vkey,"config"])


class VendorCLI(click.MultiCommand):
    """This provides the actual commands for the app by interleaving the
    top level control commands, such as `new` and `config` with the vendor
    specific command suites.
    """
    def list_commands(self, ctx):
        """ create a list of commands from the list of vendor keys, sorted,
        and the global commands prepended
        """
        # this will provide a sorted list of vendors
        commands=getAvailableVendorKeys()
        
        # we append the next four, in this order, to the front of the list
        # this yields a list with 'non-vendor' commands in the front, and
        # the alphabetically sorted list of vendors following
        commands.insert(0,'config')
        commands.insert(1,'add')
        commands.insert(2,'new')
        return commands
        
    def get_command(self, ctx, name):
        """Return :mod:`click` commands for each command from :meth:`list_commands`
        """
        if name in getAvailableVendorKeys():
            return VendorCommands(name)
        elif name=='config':
            return click.command()(config_doctor)
        elif name=='add':
            return click.command()(add_vendor)
        elif name=='new':
            return click.command()(new_vendor)
        else:
            return None            


# This is the entry point for the dns utility.  It is defined as an entry
# point in setup.py.  This also defines the top level 'group' in the click
# nomenclature.  When a command is executed, this command will be executed,
# however, during 'help' and 'documentation' generation, the command will
# not be executed.
#
# When cli() is executed, we read the local config file and store the top
# level option values in the context.
#
# the cls=VendorCLI argument replaces the @click.group decorator.  If we use
# the @click.group decorator then we can not dynamically compute the help text
@click.command(cls=VendorCLI,help='''
    The DNS utility.  Type '%s <command> --help' for detailed help.
    Use the 'config' command to manage your global configuration
    and credentials.
    ''' % PROGNAME
)
@click.option('--config', type=click.File('r'),
              help='Credentials-and-Config file to use')
@click.option('-v', '--verbose', default=False,is_flag=True,
              help='Enables verbose mode.')
@click.help_option()
@click.version_option(version="0.0.1")
@click.pass_context
def cli(ctx,verbose,config):
    """Establish the main context for use by subcommands - the primary commands
    are handled by the VendorCLI class.  Any time dns <subcommand> is encountered,
    even if dns <subcommand> --help is provided, this is executed.
    """
    fname=config
    base_config={}
    cfg_default=click.get_app_dir(PROGNAME)
    if 'HOME' in os.environ:
        cfg_default="%s/.hapi-dns-shell" % (os.environ['HOME'])
    try:
        file=None
        if fname!=None:
            if os.access(fname,os.R_OK):
                file=open(fname)
            else:
                click.echo('Config file %s is not readable.' % fname)
        else:
            if 'DNS_CONFIG' in os.environ:
                fname=os.environ['DNS_CONFIG']
                if os.access(fname,os.R_OK):
                    file=open(fname)
            else:
                if cfg_default!=None:
                    fname=cfg_default
                if os.access(fname,os.R_OK):
                    file=open(fname)
        if verbose:
            click.echo("Loading config from %s" % fname)
        try:
            if file!=None:
                base_config=json.loads(file.read())
        except Exception as e:
            click.echo('Problem parsing config file %s' % fname)
            click.echo('Error message=%s' % e)
            click.echo('We will now run the config doctor')
            try:
                _run_config_doctor(cfg_default)
            except Exception as EE:
                print(EE)
            print("Config doctor complete")
            ctx.exit()
        finally:
            if file!=None:
                file.close()
    except Exception as e:
        if verbose:
            print(e)
        raise
        ctx.exit()

    
    email=base_config.get('email')
    lconfig=base_config.get('logging')
    if lconfig!=None:
        logging.config.dictConfig(lconfig)
    ctx.obj={
        'verbose':verbose,
        'config':base_config,
        'cfile':cfg_default,
        'email':email
        }
        

            
