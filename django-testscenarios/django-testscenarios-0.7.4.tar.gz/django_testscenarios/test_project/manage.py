#!/usr/bin/env python
# Copyright (C) 2010, 2011 Linaro Limited
#
# Author: Zygmunt Krynicki <zygmunt.krynicki@linaro.org>
#
# This file is part of django-testscenarios.
#
# django-testscenarios is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation
#
# django-testscenarios is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-testscenarios.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys


def find_sources():
    base_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../..")
    if os.path.exists(os.path.join(base_path, "django_testscenarios")):
        sys.path.insert(0, base_path)


if __name__ == "__main__":
    find_sources()
    settings_module = "django_testscenarios.test_project.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
