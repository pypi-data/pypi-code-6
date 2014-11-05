import click

from .bittivahti import Bittivahti


@click.command('bittivahti')
@click.option('--curses/--no-curses', help='EXPERIMENTAL curses mode')
@click.option('-i', '--interval', default=3, type=click.FLOAT,
              help='Wait SECONDS between updates', metavar='SECONDS')
def main(interval, curses):
    """Display traffic statistics on local network interfaces"""
    dynunit = False
    colors = False
    if curses:
        from .terminal import main
        main(update_delay=interval)
    else:
        bitti = Bittivahti()
        bitti.loop(interval, dynunit, colors)
