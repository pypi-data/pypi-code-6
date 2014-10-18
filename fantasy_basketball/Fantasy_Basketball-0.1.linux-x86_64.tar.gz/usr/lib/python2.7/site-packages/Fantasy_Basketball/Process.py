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

import os
from bs4 import BeautifulSoup
import pandas as pd
import errno

from Fantasy_Basketball import augment_minutes
from Fantasy_Basketball import augment_price
from Fantasy_Basketball import augment_value
from Fantasy_Basketball import default_raw_data_dir
from Fantasy_Basketball import default_processed_data_dir

teams = [u'SAS', u'OKC', u'CHI', u'BOS', u'PHO', u'MEM', u'ORL', u'NYK',
         u'PHI', u'NOH', u'UTA', u'ATL', u'DEN', u'IND', u'HOU', u'SAC',
         u'CHA', u'LAL', u'DET', u'BRK', u'MIN', u'GSW', u'TOR', u'POR',
         u'WAS', u'LAC', u'MIA', u'MIL', u'CLE', u'DAL', u'NOP']


def get_player_stats(data_dir, year):
   d = os.path.join(data_dir, 'raw_data', 'teams', str(year))
   pkl = os.path.join(data_dir, 'processed_data', str(year))
   mkdir_p(pkl)
   df = get_players(d, year)
   df = augment_minutes(df)
   df = augment_value(df)
   df = augment_price(df)
   pkl = os.path.join(pkl, 'team_data.pkl')
   df.to_pickle(pkl)


def get_dataframe(filename, table_id):
   with open(filename, 'r') as fd:
      soup = BeautifulSoup(fd.read())

   try:
      table = soup.find('table', {'id': table_id})
      body = table.find('tbody')
      rows = body.find_all('tr', {'class': ''})
   except AttributeError:
      print "Parsing {0} failed".format(filename)
      return df.DataFrame()

   rows = [str(r.encode('utf-8')) for r in rows if r['class'] == ['']]

   html = '<table>' + ''.join(rows) + '</table>'

   df = pd.io.html.read_html(html, infer_types=False)[0]

   return df


def get_advanced(data_dir, year):

   df = pd.DataFrame()

   cols = ['Rk', 'Player', 'Age', 'G', 'MP', 'PER', 'TS%', 'eFG%', 'FTr',
           '3PAr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%',
           'USG%', 'ORtg', 'DRtg', 'OWS', 'DWS', 'WS', 'WS/48']

   for t in teams:
      filename = os.path.join(data_dir, "{0}.html".format(t))
      if os.path.isfile(filename):
         tmp = get_dataframe(filename, 'advanced')
         tmp.columns = cols
         tmp['year'] = int(year)
         df = df.append(tmp)

   del df['Rk']
   del df['Age']
   del df['G']
   df['PER'] = df['PER'].astype(float)
   df['TS%'] = df['TS%'].astype(float)
   df['eFG%'] = df['eFG%'].astype(float)
   df['FTr'] = df['FTr'].astype(float)
   df['3PAr'] = df['3PAr'].astype(float)
   df['ORB%'] = df['ORB%'].astype(float)
   df['DRB%'] = df['DRB%'].astype(float)
   df['TRB%'] = df['TRB%'].astype(float)
   df['AST%'] = df['AST%'].astype(float)
   df['STL%'] = df['STL%'].astype(float)
   df['BLK%'] = df['BLK%'].astype(float)
   df['TOV%'] = df['TOV%'].astype(float)
   df['USG%'] = df['USG%'].astype(float)
   df['ORtg'] = df['ORtg'].astype(float)
   df['DRtg'] = df['DRtg'].astype(float)
   df['OWS'] = df['OWS'].astype(float)
   df['DWS'] = df['DWS'].astype(float)
   df['WS'] = df['WS'].astype(float)
   df['WS/48'] = df['WS/48'].astype(float)

   return df


def get_pergame(data_dir, year):

   df = pd.DataFrame()

   cols = ['ind', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
           '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB',
           'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

   for t in teams:
      filename = os.path.join(data_dir, "{0}.html".format(t))
      if os.path.isfile(filename):
         tmp = get_dataframe(filename, 'per_game')
         tmp.columns = cols
         tmp['year'] = int(year)
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
   del df['ind']

   return df


def get_salaries(data_dir, year):
   df = pd.DataFrame()

   cols = ['ind', 'Player', 'Salary']

   for t in teams:
      filename = os.path.join(data_dir, "{0}.html".format(t))
      if os.path.isfile(filename):
         tmp = get_dataframe(filename, 'salaries')
         tmp.columns = cols
         tmp['year'] = int(year)
         df = df.append(tmp, ignore_index=True)

   df['Salary'] = df['Salary'].str.replace(r'[$,]', '').astype('float')
   del df['ind']

   return df


def get_roster(data_dir, year):
   df = pd.DataFrame()

   cols = ['No.', 'Player', 'Pos', 'Ht', 'Wt',
           'Birth Date', 'Experience', 'College']

   for t in teams:
      filename = os.path.join(data_dir, "{0}.html".format(t))
      if os.path.isfile(filename):
         tmp = get_dataframe(filename, 'roster')
         tmp.columns = cols
         tmp['year'] = year
         df = df.append(tmp)

   del df['No.']

   # replace positions so that only C-PF-SF-SG-PG exist
   replacement = {"Pos": {'PF-SF': 'PF', 'PG-SG': 'PG', 'PG-SG': 'PG',
                          'SF-PF': 'SF', 'SF-SG': 'SF', '^G$': 'SG',
                          'G-F': 'SG', 'F': 'PF', 'G-PF': 'G'}}
   df.replace(to_replace=replacement, inplace=True)

   # set height to be in inches for all players
   def tmp(s):
      t = s.split('-')
      return int(t[0]) * 12 + int(t[1])

   df['Experience'].replace('R', 0, inplace=True)
   df['Ht'] = df['Ht'].apply(tmp)

   df['Wt'] = df['Wt'].astype(int)

   return df


def get_players(data_dir, year):
   df1 = get_roster(data_dir, year)
   df2 = get_pergame(data_dir, year)
   df3 = get_salaries(data_dir, year)
   df4 = get_advanced(data_dir, year)
   del df2['year']
   del df3['year']
   del df4['year']
   df5 = pd.merge(df1, df2, left_on="Player", right_on="Player", how="inner")
   df6 = pd.merge(df5, df3, left_on="Player", right_on="Player", how="inner")
   df7 = pd.merge(df6, df4, left_on="Player", right_on="Player", how="inner")
   import ipdb; ipdb.set_trace()

   df7['MP'] = df7['MP_x']

   del df7['MP_x']
   del df7['MP_y']
   return df7


def htmlToPandas(filename, name):

   cols = ['Season', 'Lg', 'Team', 'W', 'L', 'W/L%', 'Finish', 'SRS', 'Pace',
           'Rel_Pace', 'ORtg', 'Rel_ORtg', 'DRtg', 'Rel_DRtg', 'Playoffs',
           'Coaches', 'WS']

   df = get_dataframe(filename, name)

   df.columns = cols

   df['WS'].replace(r'\xc2\xa0',
                    value=' ',
                    inplace=True,
                    regex=True)
   df['Team'] = name
   df['Season'].replace(r'-\d\d$',
                        value='',
                        inplace=True,
                        regex=True)
   df['Season'] = df['Season'].astype(int)
   df['W'] = df['W'].astype(int)
   df['L'] = df['L'].astype(int)
   df['W/L%'] = df['W/L%'].astype(float)
   df['Finish'] = df['Finish'].astype(float)
   df['SRS'] = df['SRS'].astype(float)
   df['Pace'] = df['Pace'].astype(float)
   df['Rel_Pace'] = df['Rel_Pace'].astype(float)
   df['ORtg'] = df['ORtg'].astype(float)
   df['Rel_ORtg'] = df['Rel_ORtg'].astype(float)
   df['DRtg'] = df['DRtg'].astype(float)
   df['Rel_DRtg'] = df['Rel_DRtg'].astype(float)

   with open('tmp.html', 'w') as fd:
      fd.write(df.to_html().encode('utf-8'))

   return df
