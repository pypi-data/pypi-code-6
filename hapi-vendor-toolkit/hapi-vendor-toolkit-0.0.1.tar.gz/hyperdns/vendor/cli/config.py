import click,json,os
from hyperdns.vendor.core import (
    import_driver,
    getAvailableVendorKeyNameTuples
    )

def _configure_vendors(config):
    """run through the set of available vendors and configure
    as requested - each driver provides a list of properties to
    be configured.  there is no support for validation or
    password-hiding at this point.
    
    :param dict config: the existing config dict.  Note that entries
       will be deleted from the config if the user decides not to
       keep that config.
    :return: <vkey> mapped dict of driver configurations 
    :rtype: dict
       
    """
    if config==None:
        config={}
    
    for vkey,vname in getAvailableVendorKeyNameTuples():
        doConfig=click.confirm("Would you like to configure '%s'" % vname)
        if doConfig:
            dclass=import_driver(vkey,verbose=True)
            if dclass==None:
                click.echo("Unable to load the driver class for '%s'" % vname)
            else:
                cfg=config.setdefault(vkey,{})
                params=dclass.info.get('settings',[])
                for p in params:
                    cfg[p]=click.prompt("%s %s" % (dclass.name,p),default=cfg.get(p,''))
        else:
            if config.get(vkey)!=None:
                delConfig=click.confirm("You have an existing configuration for '%s',\n"\
                                        "   would you like to delete it?" % vname)
                if delConfig:
                    del config[vkey]
    return config

def _configure_logging(config):
    """Let the user know what we're doing with logging - either preserving the
    existing configuration or setting up a simple, basic logging.
    
    :param dict config: The existing configuration, if any.
    :return: configuration suitable for :mod:`logging.config` :meth:`dictConfig`
    :rtype: dict
    """
    if config!=None:
        click.echo("We are preserving your existing logging config")
    else:
        click.echo("We are configuring default logging automatically.")
        click.echo("Please manuall edit your configuration and adjust as desired")
        config={
            'version': 1,              
            'formatters': {
                'cli': {
                    'format': '%(name)s: %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level':'INFO',    
                    'class':'logging.StreamHandler',
                },  
            },
            'loggers': {
                '': {                  
                    'handlers': ['console'],        
                    'level': 'DEBUG',  
                    'propagate': True  
                }
            }
        }
    
    return config
                     
def _run_config_doctor(cfile):
    """Interactive configuration of vendors.  This will load a configuration
    file, allow configuration of the default email and then it will
    scan through each of the available vendors and ask about those settings.
    The file will then be written in one fell swoop as a formatted JSON dump.
    
    :param path cfile: Path to the target cfile
    """
    
    # read in the existing configuration.
    config=None
    try:
        config=json.loads(open(cfile,'r').read())
        click.echo("Loaded config from %s" % cfile)
    except Exception as E:
        pass
    if config==None:
        config={}
        
    # make sure we can write
    canOpen=False
    while not canOpen:
        try:
            canOpen=os.access(cfile,os.W_OK) or not os.access(cfile,os.F_OK)
            if not canOpen:
                raise Exception("Unknown reason, can not open '%s'" % cfile)
        except Exception as E:
            click.echo("Sorry, I can not open '%s' for writing: %s" % (cfile,E))
            cfile=click.prompt("Please provide a new filename",default=cfile)

    # configure top level settings
    config['email']=click.prompt("Default email (for zone creation):",
        default=config.get('email'))
    
    # configure logging
    config['logging']=_configure_logging(config.get('logging'))

    # configure vendors
    config['vendors']=_configure_vendors(config.get('vendors'))

    # save the file out
    click.echo("Writing %s" % cfile)
    with open(cfile,'w+') as openfile:
        openfile.write(json.dumps(config,sort_keys=True,
                      indent=4, separators=(',', ': ')))
                      

@click.pass_obj
def config_doctor(obj):
    """This is a :mod:`click` wrapper around the :meth:`_run_config_doctor`
    method, which can be invoked from a non :mod:`click` sources, such as
    when a config is identified as absent.
    """
    _run_config_doctor(obj.get('cfile','HAPI-VENDOR-TOOLKIT.CONFIG'))
