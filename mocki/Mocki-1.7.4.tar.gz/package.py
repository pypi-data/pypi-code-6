#
#   Copyright 2011 Olivier Kozak
#
#   This file is part of Mocki.
#
#   Mocki is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
#   version.
#
#   Mocki is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License along with Mocki. If not, see
#   <http://www.gnu.org/licenses/>.
#

import os


def get_version():
    with open(os.path.join(os.path.dirname(__file__), 'version'), 'r') as file_:
        return file_.read().strip()


def load_readme_file():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as file_:
        return file_.read()
