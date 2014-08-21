from __future__ import print_function

import click
import os
import shutil
import tempfile

from . import builder
from . import paths


@click.group()
def cli():
    pass


def run_http_server(folder):

    os.chdir(folder)

    import SimpleHTTPServer
    import SocketServer

    class Daemon(SocketServer.TCPServer):
        allow_reuse_address = True

    PORT = 8000

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = Daemon(("127.0.0.1", PORT), Handler)

    print ("serving at port", PORT)

    httpd.serve_forever()
    httpd.shutdown()


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
        run_http_server(output)


@cli.command()
def demo():
    """ Build the example and show it in the browser. """

    current_dir = os.getcwd()

    try:
        output = tempfile.mkdtemp()

        os.chdir(paths.get_example_path())
        builder.build_site(output)

        run_http_server(output)
    finally:
        os.chdir(current_dir)
        shutil.rmtree(output)


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
