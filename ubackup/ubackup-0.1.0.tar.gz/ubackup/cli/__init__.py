from ubackup import settings, utils, log
from ubackup.bucket import BUCKETS
from ubackup.manager import Manager
from ubackup.cli import actions
import click

import logging
logger = logging.getLogger(__name__)


@click.group(cls=actions.Actions)
@click.version_option(settings.VERSION)
@click.pass_context
@click.option(
    '--settings-path',
    help='Path to your settings which will be merged with the app settings.')
@click.option(
    '--bucket',
    help='The bucket you want to use.',
    type=click.Choice(BUCKETS.keys()),
    required=True)
@click.option(
    '--log-level',
    help='The log level you want to capture.',
    type=click.Choice(log.level_names()),
    default='INFO')
def cli(ctx, settings_path, bucket, log_level):
    # Merge settings and init logging
    utils.merge_settings(settings_path)
    log.set_level(log_level)

    ctx.obj['manager'] = Manager(BUCKETS[bucket]())


# -----


def main():
    log.set_config(settings.LOGGING)
    try:
        cli(obj={})
    except Exception as e:
        logger.error(e, exc_info=True)
