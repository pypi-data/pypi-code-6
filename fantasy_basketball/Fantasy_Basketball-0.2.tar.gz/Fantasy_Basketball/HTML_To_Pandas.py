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

import copy
import pycurl
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
