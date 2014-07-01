import click
import json
import logging
from vl.commands import cloud_provider as cmd_cloud_provider


@click.group('cloud-provider')
def cloud_provider():
    """
    Cloud provider commands
    """
    logger = logging.getLogger(__name__)
    logger.debug('Cloud provider commands...')


@cloud_provider.command('list')
@click.option('-n', '--name', help='optional cloud provider name')
def list_cloud_providers(name):
    """
    List cloud provider details
    """
    logger = logging.getLogger(__name__)
    logger.debug('List cloud provider...')

    result = cmd_cloud_provider.list_cloud_providers(name)
    click.echo(json.dumps(result))
