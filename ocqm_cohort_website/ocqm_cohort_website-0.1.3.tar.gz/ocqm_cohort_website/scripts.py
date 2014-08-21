from __future__ import print_function

import click
import os

from . import builder
from . import paths
from . import server


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '--output',
    help="folder to write the html to",
    default=None
)
@click.option(
    '--serve/--no-serve',
    help="serve resulting files",
    default=False
)
def build(output, serve):
    """ Builds the cohort in the current directory and write the resulting
    html files in the output folder (./output by default).

    """

    if not output:
        output = os.path.join(os.getcwd(), 'output')

    builder.build_site(output)

    if serve:
        server.run_http_server(output)


@cli.command()
def demo():
    """ Build the example and show it in the browser. """

    with paths.temporary_directory() as output:

        with paths.switch_path(output):
            builder.build_site(output)

        server.run_http_server(output)


@cli.command()
def init():
    """ Initialize a new cohort in the current folder. """

    if os.listdir('.'):
        print("The current folder must be empty!")
        return

    paths.copy_files(paths.get_example_path(), '.')
    print("done")


# integrated through setup.py
commands = click.CommandCollection(sources=[cli])
