__author__ = "Alok Kumar"

from .today import today, tomorrow
from .summary import summary
from .current import current
import click


@click.group()
def cli():
    pass

cli.add_command(today)
cli.add_command(current)
cli.add_command(summary)
cli.add_command(tomorrow)