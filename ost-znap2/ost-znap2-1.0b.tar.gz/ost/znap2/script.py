"""
Console script for Zodb manipulations.
"""

import click
import sys
import functools
from .storage import Storage


def die(message):
    """Print message to stderr and exit with code 1."""
    click.echo(message, file=click.get_text_stream('stderr'))
    sys.exit(1)


def error_reporter(func):
    """Error reporting decorator."""
    @functools.wraps(func)
    def wrapped(*args, **kw):
        try:
            return func(*args, **kw)
        except ValueError, err:
            die(str(err))
        except (OSError, IOError), err:
            if '.znap2' in str(err):
                die('No .znap2 subdirectory found. '
                    'Probably storage not initialized.')
    return wrapped


def storage_passer(func):
    """Error reporting decorator."""
    @functools.wraps(func)
    def wrapped(*args, **kw):
        kw['storage'] = Storage('.')
        kw['storage'].load()
        return func(*args, **kw)
    return wrapped


@click.group()
def main():
    """Make and restore ZoDB snapshots."""


@main.command()
@click.argument('databases', nargs=-1, required=True)
def init(databases):
    """Initialize the storage."""
    st = Storage('.')
    for database in databases:
        st.add(database)
    st.init()


@main.command()
@click.argument('snapshot_id', required=True)
@error_reporter
@storage_passer
def save(storage, snapshot_id):
    """Save the current state of the database(s)."""
    storage.save(snapshot_id)


@main.command()
@error_reporter
@storage_passer
def list(storage):
    """List existing snapshots."""
    for item in storage.list():
        print item.id


@main.command()
@click.argument('snapshot_id', required=True)
@error_reporter
@storage_passer
def restore(storage, snapshot_id):
    """Restore the database(s) to a snapshot."""
    storage.restore(snapshot_id)


@main.command()
@click.argument('snapshot_id', required=True)
@error_reporter
@storage_passer
def delete(storage, snapshot_id):
    """Delete a snapshot."""
    storage.delete(snapshot_id)
