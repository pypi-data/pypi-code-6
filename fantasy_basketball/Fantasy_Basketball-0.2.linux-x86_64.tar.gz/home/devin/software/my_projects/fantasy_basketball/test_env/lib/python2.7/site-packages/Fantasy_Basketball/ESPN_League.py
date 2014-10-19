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

import pycurl
import pandas as pd
from bs4 import BeautifulSoup


class ESPN(object):

   def __init__(self, year, leagueID):
      """
         init ESPN object

         :param year: The year that league takes place
         :param leagueID: The ESPN league ID
      """

      self.processLeague()

   def processLeague(self):
      """
         extract info from standings and league info, place into dataframe
      """

      self.teams = {}
      soup = BeautifulSoup(self.standingsBuf.getvalue())
      tables = soup.findAll("table")

      for table in tables:
         if table.findAll(text='EAST'):
            east = table
         if table.findAll(text='WEST'):
            west = table

      teams = east.findAll('tr')[2:]
      for t in teams:
         cols = t.findAll('td')
         d = {}
         d['wins'] = int(cols[1].text)
         d['losses'] = int(cols[2].text)
         d['ties'] = int(cols[3].text)
         d['conf'] = 'east'
         teamName = (cols[0].text).lower()
         self.teams[teamName] = d

      teams = west.findAll('tr')[2:]
      for t in teams:
         cols = t.findAll('td')
         d = {}
         d['wins'] = int(cols[1].text)
         d['losses'] = int(cols[2].text)
         d['ties'] = int(cols[3].text)
         d['conf'] = 'west'
         teamName = (cols[0].text).lower()
         self.teams[teamName] = d

      soup = BeautifulSoup(self.leagueBuf.getvalue())
      tables = soup.findAll("table", attrs={"class": "playerTableTable"})
      for table in tables:
         teamName = table.findAll('tr')[0].findAll('a')[0].text
         teamName = teamName.lower()
         rows = table.findAll('tr')[2:]
         players = []
         for row in rows:
            try:
               player = row.findAll('a')[0].text
               players.append(player)
            except:
               pass

         self.teams[teamName]['players'] = players
