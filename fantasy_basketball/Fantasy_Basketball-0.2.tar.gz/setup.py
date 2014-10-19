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
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
   return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="Fantasy_Basketball",
      version="0.2",
      author="Devin Kelly",
      author_email="dwwkelly@fastmail.fm",
      description=("A package that fetches, processes and visualizes " +
                   "fantasy basketball statistics"),
      license="GPL3",
      keywords = "fantasy basketball pandas",
      url = "https://github.com/dwwkelly/fantasy_basketball",
      test_suite="tests",
      scripts=['scripts/FB_Manager.py'],
      long_description=read('README.rst'),
      packages=find_packages(),
      include_package_data=True,
      install_requires=['Click', 'numpy', 'matplotlib',
                        'pandas', 'jinja2', 'pycurl',
                        'beautifulsoup4', 'lxml'],
      )
