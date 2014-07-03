import click
import json
import logging
from vl.commands import cloud_account as cmd_cloud_account


@click.group('cloud-account')
def cloud_account():
    """
    Cloud account commands
    """
    logger = logging.getLogger(__name__)
    logger.debug('Cloud account commands...')


@cloud_account.command()
@click.option('-c', '--cloud-provider', 'cloud_provider', prompt=True, help='cloud provider name')
@click.option('-n', '--name', prompt=True, help='cloud account name')
@click.option('-k', '--api-key', 'api_key', prompt=True, hide_input=True, help='api key')
@click.option('-s', '--api-secret', 'api_secret', prompt=True, hide_input=True, help='api secret')
def add(cloud_provider, name, api_key, api_secret):
    """
    Register a new cloud account
    """
    logger = logging.getLogger(__name__)
    logger.debug('Adding cloud account...')
    logger.debug('Cloud Provider: %s, Name: %s', cloud_provider, name)

    result = cmd_cloud_account.add(cloud_provider, name, api_key, api_secret)
    click.echo(json.dumps(result))


@cloud_account.command('list')
@click.option('-n', '--name', help='optional cloud account name')
def list_cloud_accounts(name):
    """
    List cloud account details
    """
    logger = logging.getLogger(__name__)
    logger.debug('List cloud accounts...')

    result = cmd_cloud_account.list_cloud_accounts(name)
    click.echo(json.dumps(result))


@cloud_account.command()
@click.option('-n', '--name', prompt=True, help='current cloud account name')
@click.option('-a', '--new-name', 'new_name', help='new cloud account name')
@click.option('-k', '--new-api-key', 'new_api_key', hide_input=True, help='new api key')
@click.option('-s', '--new-api-secret', 'new_api_secret', hide_input=True, help='new api secret')
def update(name, new_name, new_api_key, new_api_secret):
    """
    Update an existing cloud account
    """
    logger = logging.getLogger(__name__)
    logger.debug('Updating cloud account...')
    logger.debug('Name: %s', name)

    result = cmd_cloud_account.update(name, new_name, new_api_key, new_api_secret)
    click.echo(json.dumps(result))


@cloud_account.command()
@click.option('-n', '--name', prompt=True, help='current cloud account name')
def delete(name):
    """
    Delete an existing cloud account
    """
    logger = logging.getLogger(__name__)
    logger.debug('Deleting cloud account...')
    logger.debug('Name: %s', name)

    result = cmd_cloud_account.delete(name)
    click.echo(json.dumps(result))
