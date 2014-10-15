import click
import subprocess
from hyperdns.vendor.core import import_driver

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
            dclass=import_driver(vkey)
            if dclass==None:
                click.echo("Successfully installed but something is not correct. Could not import %s" % vkey)
            else:
                cli.main(args=[vkey,'config'])



