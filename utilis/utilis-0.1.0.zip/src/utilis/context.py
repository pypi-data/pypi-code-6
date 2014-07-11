#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Utilis Tasks
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Utilis Tasks.
#
# Hive Utilis Tasks is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Utilis Tasks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Utilis Tasks. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import jinja2

def run():
    if not len(sys.argv) > 1:
        print("Invalid number of arguments")
        return 2

    path = sys.argv[1]
    path = os.path.abspath(path)
    path = os.path.normpath(path)

    base, file = os.path.split(path)

    loader = jinja2.FileSystemLoader(base)
    environment = jinja2.Environment(loader = loader)
    template = environment.get_template(file)

    result = template.render(**os.environ)
    print(result)
