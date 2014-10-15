import json,click
from hyperdns.hapi.client.cli import main

#
@main.command()
@click.option('--scan','what',flag_value='scan_all_vendors',help="Scan all available vendors")
@click.option('--prune','what',flag_value='prune_stale_scans',help="Prune scans")
@click.option('--validate','what',flag_value='validate_on_nameservers',help="Validate on nameservers")
@click.pass_obj
def task(hapi,what):
    """Spawn background tasks
    """
    result=hapi.task(what)
    click.echo(result)