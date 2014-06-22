"""
CLI Driver
"""

import click
import logging
import vl
from logging.config import dictConfig
from vl.config.logging import get_config
from user import user


def setup_logging(ctx, param, value):
    dictConfig(get_config(value))


def show_version(ctx, param, value):
    if value:
        click.echo('version %s' % vl.__version__)
        ctx.exit()


@click.group()
@click.option('-d', '--debug', is_flag=True, callback=setup_logging, expose_value=False,
              help='turn on debug logging')
@click.option('-v', '--version', is_flag=True, callback=show_version, expose_value=False,
              help='display the version number')
def run():
    """
    Command line interface to VeraxLabs REST API's
    """
    logger = logging.getLogger(__name__)
    logger.debug('Processing command line...')


run.add_command(user)
