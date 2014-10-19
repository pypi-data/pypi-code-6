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

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

def gen_web(data_dir, df):
   pages = []
   p.append(get_value_page(df))

def get_value_page(df):
   p = {'title': 'Value Data',
        'obj': df,
        'fantasyID': 'value',
        'href': 'value-data.html',
        'cols': ['rank', 'Player', 'Pos', 'FTeam', 'Tm', 'G',
        'GS', 'MP', 'FG%', 'FT%', 'TRB', 'AST', 'STL',
        'BLK', 'PTS', 'NormalizedValue', 'NaiveValue']}
   return p


def process_pages(df):
   j2_env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
   baseTemplate = j2_env.get_template('fantasy-template.html')
   tocTemplate = j2_env.get_template('toc.html')
   posTemplate = j2_env.get_template('positional-template.html')
   chartsTemplate = j2_env.get_template('charts-template.html')

   expr1 = re.compile(r"<tr>.*rank.*</thead>", re.MULTILINE | re.DOTALL)
   expr2 = re.compile(r"<tr>.*Pos.*</thead>", re.MULTILINE | re.DOTALL)
   expr3 = re.compile(r"<tr>.*FTeam.*</thead>", re.MULTILINE | re.DOTALL)

   for p in pages:
      fantasyID = p['fantasyID']
      htmlText = p['obj'].to_html(columns=p['cols'],
                                  classes=["table", "table-bordered"])

      if fantasyID == 'pb-mean':
         expr = expr2
      elif fantasyID == 'teamValue':
         expr = expr3
      else:
         expr = expr1

      tmp = ('normalized-value-positional' == fantasyID) or \
      ('rosters' == fantasyID)

      if tmp:
         for k in htmlText.keys():
            newKey = re.sub(r'\s', '_', k)
            newKey = re.sub(r'\+', '_', newKey)
            htmlText.rename({k: newKey}, inplace=True)

         for k in htmlText.keys():
               txt = htmlText[k][:7]
               htmlText[k] = txt
               htmlText[k] += 'id="{0}" '.format(k)
               htmlText[k] += txt
               htmlText[k] = re.sub(expr, "</thead>", htmlText[k])
         template = posTemplate
      else:
         htmlText = htmlText[:7] + 'id="{0}" '.format(fantasyID) + htmlText[7:]
         htmlText = re.sub(expr, "</thead>", htmlText)
         template = baseTemplate

      with open(os.path.join(self.filesPath, p['href']), 'w') as fd:
         text = template.render(title=p['title'],
                                fantasy_table=htmlText,
                                fantasy_id=fantasyID,
                                allPages=pages)
         fd.write(text)

      with open(os.path.join(self.filesPath, 'charts.html'), 'w') as fd:
         text = chartsTemplate.render(title='Charts',
                                      figs=self.figures,
                                      allPages=pages)
         fd.write(text)

      with open(os.path.join(self.filesPath, 'toc.html'), 'w') as fd:
         text = tocTemplate.render(title='Table of Contents',
                                   pages=pages,
                                   chartsUrl='charts.html',
                                   allPages=pages)
         fd.write(text)
