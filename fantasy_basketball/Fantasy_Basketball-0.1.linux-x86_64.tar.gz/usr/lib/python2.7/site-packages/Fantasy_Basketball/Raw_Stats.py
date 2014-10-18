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

import copy
import cStringIO
import re
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', None)
pd.set_option('display.precision', 4)
htmlRoot = "html/"
minimumMinutesPlayed = 200

data_dir = 'html_data'


class RawStats(object):

   def __init__(self):
      self.url = "www.basketball-reference.com/leagues/NBA_2014_totals.html"
      self.csvName = 'nba_stats.csv'
      self.columns = ['', 'Rk', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS',
                      'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P',
                      '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB',
                      'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'FTeam']

      if not os.path.isfile(self.csvName):
         self.downloadHTML()
         self.processHTML()
         self.writeCSV()
      else:
         self.data = pd.read_csv(self.csvName)
         self.data.columns = self.columns

      self.data.fillna(0.0)
      replacement = {"Pos": {'PF-SF': 'PF', 'PG-SG': 'PG', 'PG-SG': 'PG',
                     'SF-PF': 'SF', 'SF-SG': 'SF', '^G$': 'SG'}}
      self.data.replace(to_replace=replacement, inplace=True, regex=True)

      return

   def writeCSV(self):
      self.data.to_csv(self.csvName)

   def downloadHTML(self):
      self.downloadDrafts()
      self.downloadDrafts()

   def downloadDrafts(self):

      years = range(1950, 2014)
      years.reverse()

      for y in years:
         downloadDraft(y)
         time.sleep(10.0)

   def downloadTeams(self):

      teams = [u'SAS', u'OKC', u'CHI', u'BOS', u'PHO', u'MEM', u'ORL', u'NYK',
               u'PHI', u'NOH', u'UTA', u'ATL', u'DEN', u'IND', u'HOU', u'SAC',
               u'CHA', u'LAL', u'DET', u'BRK', u'MIN', u'GSW', u'TOR', u'POR',
               u'WAS', u'LAC', u'MIA', u'MIL', u'CLE', u'DAL']

      for y in ['2013', '2014', '2012']:
         for t in teams:
            print "downloading {0}, {1}".format(t, y)
            self.downloadTeam(t, y)
            time.sleep(10.0)

   def processHTML(self):
      """ Finds the table in the downloaded HTML and converts it into a CSV """

      soup = BeautifulSoup(self.buf.getvalue())
      table = soup.find("table")

      thead = table.findAll("thead")[0]
      tbody = table.findAll("tbody")[0]

      labels = [th.getText() for th in thead.findAll("th")]
      rows = tbody.findAll("tr")

      self.stats = pd.DataFrame(columns=labels)

      tmpStats = []

      for row in rows:
         if row.find('th') is not None:
            continue
         vals = [td.getText() for td in row.findAll("td")]
         # if no statistic, fill with 0
         vals = [0 if w == '' else w for w in vals]
         tmpStats.append(dict(zip(labels, vals)))

      self.data = pd.DataFrame(columns=labels, data=tmpStats, dtype=float)
      self.data = self.data[self.data.MP > minimumMinutesPlayed]
      self.data[u'FTeam'] = 'FA'

      ############
      all_teams = pd.DataFrame()

      for t in teams:
         print t
         df = htmlToPandas('html/{team}.html'.format(team=t), t)
         all_teams = pd.concat([all_teams, df])

      ###############
         with open(filename, 'r') as fd:
            soup = BeautifulSoup(fd.read())

         try:
            table = soup.find('table', {'id': table_id})
            body = table.find('tbody')
            rows = body.find_all('tr', {'class': ''})
         except AttributeError:
            print "Parseing {0} failed".format(filename)
            return df.DataFrame()

         rows = [str(r.encode('utf-8')) for r in rows if r['class'] == ['']]

         html = '<table>' + ''.join(rows) + '</table>'

         df = pd.io.html.read_html(html, infer_types=False)[0]

         return df

      ####################

         df = pd.DataFrame()

         for t in teams:
            for y in years:
               fname = "html/{0}_{1}.html".format(t, y)
               tmp = get_dataframe(fname, 'per_game')
               tmp.columns = cols
               tmp['year'] = int(y)
               df = df.append(tmp)

         df['Age'] = df['Age'].astype(int)
         df['G'] = df['G'].astype(int)
         df['GS'] = df['GS'].astype(int)
         df['MP'] = df['MP'].astype(float)
         df['FG'] = df['FG'].astype(float)
         df['FGA'] = df['FGA'].astype(float)
         df['FG%'] = df['FG%'].astype(float)
         df['3P'] = df['3P'].astype(float)
         df['3PA'] = df['3PA'].astype(float)
         df['3P%'] = df['3P%'].astype(float)
         df['2P'] = df['2P'].astype(float)
         df['2PA'] = df['2PA'].astype(float)
         df['2P%'] = df['2P%'].astype(float)
         df['FT'] = df['FT'].astype(float)
         df['FTA'] = df['FTA'].astype(float)
         df['FT%'] = df['FT%'].astype(float)
         df['ORB'] = df['ORB'].astype(float)
         df['DRB'] = df['DRB'].astype(float)
         df['TRB'] = df['TRB'].astype(float)
         df['AST'] = df['AST'].astype(float)
         df['STL'] = df['STL'].astype(float)
         df['BLK'] = df['BLK'].astype(float)
         df['TOV'] = df['TOV'].astype(float)
         df['PF'] = df['PF'].astype(float)
         df['PTS'] = df['PTS'].astype(float)

         return df
