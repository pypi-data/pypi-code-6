#!/usr/bin/env python
#  Copyright (C) 2014 Devin Kelly
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Devin Kelly"

import os
import time
import click
import errno

from Fantasy_Basketball import download_data
from Fantasy_Basketball import get_player_stats
from Fantasy_Basketball import default_dir
from Fantasy_Basketball import default_raw_data_dir
from Fantasy_Basketball import default_processed_data_dir
from Fantasy_Basketball import default_plot_dir
from Fantasy_Basketball import default_html_dir
from Fantasy_Basketball import mkdir_p
from Fantasy_Basketball import Plotter


@click.group()
def cli():
   pass


@cli.command()
@click.option('--data_dir',
              default=default_dir,
              help='Download Fantasy Basketball Data')
@click.option('--teams', is_flag=True, default=False,
              help="Download NBA Team Data Only")
@click.option('--draft', is_flag=True, default=False,
              help="Download Draft Data Only")
@click.option('--league', is_flag=True, default=False,
              help="Download Fantasy League Data Only")
@click.option('--year', default=time.strftime('%Y', time.localtime()),
              help="The year to use downloading stats")
@click.option('--league_id', default=None,
              help="The ESPN League ID to use downloading stats")
def download(data_dir, teams, draft, league, year, league_id):
   click.echo('Downloading to {0}'.format(data_dir))
   download_data(data_dir, teams, draft, league, year, league_id)


@cli.command()
@click.option('--data_dir',
              default=default_dir,
              help='Process Fantasy Basketball Data')
@click.option('--teams', is_flag=True, default=False,
              help="Process NBA Team Data Only")
@click.option('--draft', is_flag=True, default=False,
              help="Process Draft Data Only")
@click.option('--league', is_flag=True, default=False,
              help="Process Fantasy League Data Only")
@click.option('--year', default=time.strftime('%Y', time.localtime()),
              help="The year to use downloading stats")
def process(data_dir, teams, draft, league, year):
   click.echo('Processing to {0}'.format(data_dir))
   get_player_stats(data_dir, year)


@cli.command()
@click.option('--data_dir',
              default=default_dir,
              help='Process Fantasy Basketball Data')
@click.option('--teams', is_flag=True, default=False,
              help="Write HTML for NBA Team Data Only")
@click.option('--draft', is_flag=True, default=False,
              help="Write HTML for Draft Data Only")
@click.option('--league', is_flag=True, default=False,
              help="Write HTML for Fantasy League Data Only")
def write_html(data_dir):
   click.echo('Writing HTML Data to {0}'.format(data_dir))


@cli.command()
@click.option('--data_dir',
              default=default_dir,
              help='Process Fantasy Basketball Data')
@click.option('--year', default=time.strftime('%Y', time.localtime()),
              help="The year to use downloading stats")
def plot(data_dir, year):
   click.echo('Plotting to {0}'.format(data_dir))
   plotter = Plotter(data_dir, year)
   plotter.make_all_plots()


def main():
   cli()

   return

if __name__ == "__main__":
   main()
