from ubackup import validators
from ubackup.cli import cli
from ubackup.creator.path import PathCreator
from ubackup.creator.mysql import MysqlCreator
import click

import logging
logger = logging.getLogger(__name__)


@cli.group()
@click.pass_context
def backup(ctx):
    pass


@backup.command()
@click.pass_context
@click.option(
    '--path',
    help='Path of the backup if you want a path backup.',
    callback=validators.directory,
    required=True)
def path(ctx, path):
    ctx.obj['manager'].push_backup(PathCreator(path=path))


@backup.command()
@click.pass_context
@click.option(
    '--databases',
    help='List of MySQL databases you want to backup, "*" for all.',
    callback=validators.mysql_databases)
def mysql(ctx, databases):
    ctx.obj['manager'].push_backup(MysqlCreator(databases=databases))
