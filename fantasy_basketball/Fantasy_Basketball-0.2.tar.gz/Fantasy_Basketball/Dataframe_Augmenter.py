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

import pandas as pd
import re
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

__author__ = "Devin Kelly"

teams = [u'SAS', u'OKC', u'CHI', u'BOS', u'PHO', u'MEM', u'ORL', u'NYK',
         u'PHI', u'NOH', u'UTA', u'ATL', u'DEN', u'IND', u'HOU', u'SAC',
         u'CHA', u'LAL', u'DET', u'BRK', u'MIN', u'GSW', u'TOR', u'POR',
         u'WAS', u'LAC', u'MIA', u'MIL', u'CLE', u'DAL']

years = ['2012', '2013', '2014']


def augment_minutes(df, minutes=400):
   df = df[df.MP > minutes]
   return df


def cleanup(df):
   df = df.fillna(0.0)
   df = df.dropna()
   df = augment_minutes(df)
   return df


def augment_value(df):

   df['value'] = (df['FG%'] - df['FG%'].mean()) / df['FG%'].std() + \
                 (df['FT%'] - df['FG%'].mean()) / df['FT%'].std() + \
                 (df['TRB'] - df['TRB'].mean()) / df['TRB'].std() + \
                 (df['AST'] - df['AST'].mean()) / df['AST'].std() + \
                 (df['BLK'] - df['BLK'].mean()) / df['BLK'].std() + \
                 (df['PTS'] - df['PTS'].mean()) / df['PTS'].std()

   return df


def augment_price(df, nplayers=8, money_per_player=200, players_per_team=11):

   total_picks = nplayers * players_per_team
   money_supply = float(nplayers * money_per_player)

   df['price'] = 0.0
   years = list(set(df['year']))
   for y in years:
      top_players = df[df.year == y]
      top_players = top_players.sort('value', ascending=False)[0:total_picks]
      total_value = top_players['value'].sum()

      for ii in top_players.Player:
         player_value = top_players[top_players.Player == ii].value
         player_price = money_supply * (player_value / total_value)
         df.price[(df.year == y) & (df.Player == ii)] = player_price

   return df
