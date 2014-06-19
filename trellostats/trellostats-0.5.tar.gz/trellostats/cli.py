import os
import click

from models import Snapshot
from trellostats import TrelloStats


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
@click.argument('board')
@click.option('--cycle-time', is_flag=True,
              help='Include cycle time in report',
              default=True)
@click.option('--done', help='Title of column which represents Done\
                              to calc. Cycle Time', default="Done")
def snapshot(ctx, board, cycle_time, done):
    ctx.obj['board_id'] = board
    ts = TrelloStats(ctx.obj)
    Snapshot.create_table(fail_silently=True)
    """
        Recording mode - Daily snapshots of a board for ongoing reporting:
         -> trellis report --board=87hiudhw
                          --cycle-time
                          --spend
                          --revenue
                          --done=Done

    """
    if cycle_time:
        done_id = ts.get_list_id_from_name(done)
        cards = ts.get_list_data(done_id)
        ct = ts.cycle_time(cards)
        print ct

        # Create snapshot
        Snapshot.create(board_id=board, done_id=done_id, cycle_time=ct)


cli.add_command(snapshot)
cli.add_command(resetdb)

if __name__ == '__main__':
    cli()
