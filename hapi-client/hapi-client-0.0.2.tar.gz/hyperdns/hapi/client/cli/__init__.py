from hyperdns.hapi.client import HAPI
import re
import os
import sys
import json
import base64
import getpass
import textwrap
import cmd
import hyperdns.hal.navigator
import click
import readline
PROGNAME="hapi"

from hyperdns.netdns import (
    dotify
)
import textwrap

def nonsense(msg):
    click.echo(msg)
    click.echo("This is an internal error")

def describe_and_exit(prefix=None):
    """Uses the analysis from :meth:`_analyze_route_map` and formats
    the output.
    
    Only the uris matching the provided prefix will be printed, unles
    no prefix is provided.
    
    Todo: output formatting is pretty rough
    """
    routes=_analyze_route_map()
            
    for uri in sorted(routes.keys()):
        if prefix==None or uri.startswith(prefix):
            info=routes.get(uri)
            print(uri)
            for meth,doc in info['methods'].items():
                if doc==None:
                    doc="No documentation yet"
                elif isinstance(doc,dict):
                    doc=json.dumps(doc)
                    
                indent='      '
                print("    %s" % (meth))
                wrapper = textwrap.TextWrapper(initial_indent=indent,
                                               subsequent_indent=indent)
                print(wrapper.fill(doc))
                print()
            
    sys.exit()

def _query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
        

def _load_config(file):
    """Read the config file.  If the --config=<path> option was provided on the
    command line, attempt to use that path.  If that option was not used, then
    check the env variable HAPI_CONFIG.  If present, attempt to read the
    config from that file.  Lastly, check for $HOME/.hapi and use that
    if it is present.  If a file can not be read, or if it is corrupt, then the
    system exits with the appropriate message.
    """
    try:
        if file==None:
            if 'HAPI_CONFIG' in os.environ:
                fname=os.environ['HAPI_CONFIG']
                if os.access(fname,os.R_OK):
                    file=open(fname)
            else:
                if 'HOME' in os.environ:
                    fname="%s/.hapi" % (os.environ['HOME'])
                if os.access(fname,os.R_OK):
                    file=open(fname)

        # allow 'hapi config' to run if no config file, and autoconfig if no config file
        if file==None:
            return None
        try:
            config=json.loads(file.read())
        except Exception as e:
            prin('Problem parsing config file %s, message=%s' % (file.name,e))
            return None
        finally:
            file.close()

        assert 'jwt' in config.keys()
        assert 'baseUrl' in config.keys()
        config['fname']=file.name
        return config
    except Exception as e:
        raise
        return None
    



def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

def configurate(config):
    """
    """
    config_map={
        "baseUrl":('Base Url','http://localhost:5000/my'),
        "jwt":('JWT (Empty if you want to generate one)','')
        }
    if config==None:
        config={}
    
    click.echo("\nWelcome to the HAPI configurator!\n")
    for key in sorted(config_map.keys()):
        (label,default_value)=config_map[key]
        if key not in config.keys():
            config[key]=default_value
        label="\033[%sm%s\n>>\033[0m " % (str(32),label)
        config[key]=rlinput(label,prefill=config[key])
    
    if config.get('jwt','')=='':
        conn=rlinput('Authentication Via : ',prefill='google')
        username=rlinput('Username : ',prefill='')
        password=getpass.getpass('Password : ')
        """
           Programmatic Authentication (Service Accounts)
          A JWT can be obtained authenticating with a user from a Database or AD/LDAP connection by calling the oauth/ro endpoint of the Authentication API, passing a username, password, connection and client_id. This can be used to obtain tokens from any system without user intervention (e.g. scripts, batch files, web backends, native apps). Look under SDK - Authentication API - Database & Active Directory / LDAP Authentication (on the dashboard).
        """       
        raise Exception('not yet implemented')
        
    #d=HAPICLI(config)
    ok=True #d.login()
    if not ok:
        print("Those credentials do not work")
    else:
        save=rlinput('Would you like to save to [Y/N]? ',prefill='Y')
        if save=='Y':
            file=None
            fname=None
            if 'HOME' in os.environ:
                fname="%s/.hapi" % (os.environ['HOME'])
                if fname==None:
                    sys.exit("Missing home directory, can't find $HOME")
                with open(fname,"w") as file:
                    file.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')))
                    print("Saved config in %s" % fname)


@click.group(help='''
    The DNS utility.  Type '%s <command> --help' for detailed help.
    Use the 'config' command to manage your global configuration
    and credentials.
    ''' % PROGNAME
)
@click.option('--config', type=click.File('r'),
              help='Credentials-and-Config file to use')
@click.help_option()
@click.version_option(version="0.0.1")
@click.pass_context
def main(ctx,config):
    ctx._hapi_config_source=config
    config=_load_config(config)
    if config==None:
        print("Sorry, we can not find a valid config file.")
        print("  no config file via --config option")
        print("  no config.json in the cwd")
        print("  no HAPI_CONFIG environment variable")
        print("  no $HOME/.hapi file")
        print("------")
        if not _query_yes_no('Would you like to create $HOME/.hapi?'):
            click.echo("Gotcha, maybe next time.")
            sys.exit()
        else:
            config=configurate()
            sys.exit()
    tryAgain=True
    while tryAgain:
        try:
            jwt=config['jwt']
            baseUrl=config['baseUrl']
            ctx.obj=HAPI(jwt,baseUrl)
            return
        except Exception:
            click.echo("I can not contact the server at %s" % baseUrl)
            raise
            if _query_yes_no('Would you like to reconfigure?'):
                config=configurate(config)
            else:
                sys.exit()


def require_vendor(hapi,vkey,active=None,doexit=True):
    """Look for a vendor which must be optionally active depending upon
    the active flag.  If the vendor is not found a message is printed
    and None is returned or sys.exit() is called
    """
    vendor=hapi.vendors.get(vkey)
    if active and vendor!=None:
        if vendor.active:
            return vendor
    else:
        if vendor!=None:
            return vendor
    click.echo("I'm sorry, i can't find vendor %s in this context" % vkey)
    if doexit:
        sys.exit()
    return None

def require_zone(hapi,zone_fqdn,deleted=None,ignored=None,doexit=True):
    """Look for a vendor which must be optionally active depending upon
    the active flag.  If the vendor is not found a message is printed
    and None is returned.
    """
    zone=hapi.zones.get(dotify(zone_fqdn))

    if zone!=None:
        if deleted!=None and zone.deleted!=deleted:
            zone=None

    if zone!=None:
        if ignored!=None and zone.ignored!=ignored:
            zone=None
            
    if zone==None:
        click.echo("I'm sorry, i can't find zone %s in this context" % zone_fqdn)
        if doexit:
            sys.exit()
    return zone
        

from .shell import shell
from .hal import hal
from .ping import ping
from .zones import zones
from .vendors import vendors
from .task import task
from .resources import resources

@main.command()
@click.option('--in','upload',type=click.File('r'),default='-',help="file to load")
@click.pass_obj
def upload(hapi,upload):
    """Upload a zonefile.
    """
    
    try:
        #zone=hapi.processZoneFile(upload.read())
        zone=hapi.submitZoneFile(upload.read())
        click.echo("Zone uploaded")
    except hapi.BadCall as E:
        click.echo("Failed with code: %s" % (E.response.status_code))
 
@main.command()
@click.pass_context
def config(ctx):
    """Run the configurator"""
    config=_load_config(ctx.parent._hapi_config_source)
    configurate(config)
    
@main.command()
@click.option('--prefix',default=None,help="optional prefix")
@click.pass_obj
def docs(hapi,prefix):
    describe_and_exit(prefix=prefix)
