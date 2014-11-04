import click

from .bittivahti import Bittivahti


@click.command('bittivahti')
@click.option('-i', '--interval', default=3, type=click.FLOAT,
              help='Wait SECONDS between updates', metavar='SECONDS')
def main(interval):
    """Display traffic statistics on local network interfaces"""
    dynunit = False
    colors = False
    bitti = Bittivahti()
    bitti.loop(interval, dynunit, colors)
