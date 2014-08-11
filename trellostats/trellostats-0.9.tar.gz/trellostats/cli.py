import os
import sys
import click

from .models import Snapshot
from .trellostats import TrelloStats

# Bad, but we're dynamically calling render_ funcs
from .reports import *

def cycle_time(ts, board, done):
    done_id = ts.get_list_id_from_name(done)
    cards = ts.get_list_data(done_id)
    return ts.cycle_time(cards)


@click.group()
@click.pass_context
def cli(ctx):
    """ This is a command line app to get useful stats from a trello board
        and report on them in useful ways.

        Requires the following environment varilables:

        TRELLOSTATS_APP_KEY=<your key here>
        TRELLOSTATS_APP_TOKEN=<your token here>
    """
    ctx.obj = dict()
    ctx.obj['app_key'] = os.environ.get('TRELLOSTATS_APP_KEY')
    ctx.obj['app_token'] = os.environ.get('TRELLOSTATS_APP_TOKEN')


@click.command()
@click.pass_context
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def resetdb(ctx):
    Snapshot.drop_table()
    Snapshot.create_table()
    click.echo('Snapshots table dropped.')


@click.command()
@click.pass_context
def token(ctx):
    ts = TrelloStats(ctx.obj)
    print ts.get_token()


@click.command()
@click.argument('host')
@click.argument('port')
@click.option('--debug', is_flag=True)
def runapiserver(debug, host, port):
    from .web import app
    app.run(host=host, port=int(port), debug=debug)


@click.command()
@click.pass_context
@click.argument('board')
@click.option('--done', help='Title of column which represents Done\
                              to calc. Cycle Time', default="Done")
def snapshot(ctx, board, done):
    ctx.obj['board_id'] = board
    ts = TrelloStats(ctx.obj)
    Snapshot.create_table(fail_silently=True)
    """
        Recording mode - Daily snapshots of a board for ongoing reporting:
         -> trellis report --board=87hiudhw
                          --spend
                          --revenue
                          --done=Done

    """
    ct = cycle_time(ts, board, done)
    env = get_env()
    print render_text(env, **dict(cycle_time=ct))

    # Create snapshot
    Snapshot.create(board_id=board, done_id=done_id, cycle_time=ct)


@click.command()
@click.pass_context
@click.argument('board')
@click.option('--done', help='Title of column which represents Done\
                              to calc. Cycle Time', default="Done")
@click.option('--output', type=click.Choice(['text', 'html']), default='text', multiple=True)
def report(ctx, board, done, output):
    ctx.obj['board_id'] = board
    ts = TrelloStats(ctx.obj)
    """
        Reporting mode - Daily snapshots of a board for ongoing reporting:
         -> trellis report --board=87hiudhw
                          --spend
                          --revenue
                          --done=Done

    """
    ct = cycle_time(ts, board, done)
    env = get_env()

    #  Get all render functions from the module and filter out the ones we don't want.
    render_functions = [target for target in
                     dir(sys.modules['trellostats.reports'])
                     if target.startswith("render_") and
                     target.endswith(output)]

    for render_func in render_functions:
        print globals()[render_func](env, **dict(cycle_time=ct))


cli.add_command(snapshot)
cli.add_command(resetdb)
cli.add_command(token)
cli.add_command(report)
cli.add_command(runapiserver)
