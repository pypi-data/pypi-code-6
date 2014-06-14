#
# coding=utf-8
"""import - Import old rdial CSV data"""
from __future__ import unicode_literals
from __future__ import unicode_literals
# Copyright © 2011-2014  James Rowe <jnrowe@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import random
import time

import click

data = [random.randrange(0, 3, 0.5, _int=float) for x in range(10)]

with click.progressbar(data, label='Importing', show_pos=True,
                       item_show_func=str, width=0) as bar:
    for item in bar:
        time.sleep(item)
