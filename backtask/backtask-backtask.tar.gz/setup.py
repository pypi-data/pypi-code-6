#!/usr/bin/python -W default
#
#
# License
# -------
#
# Copyright (c) 2014 Russell Stuart
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# The copyright holders grant you an additional permission under Section 7
# of the GNU Affero General Public License, version 3, exempting you from
# the requirement in Section 6 of the GNU General Public License, version 3,
# to accompany Corresponding Source with Installation Information for the
# Program or any work based on the Program. You are still required to
# comply with all other Section 6 requirements to provide Corresponding
# Source.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
from distutils.core import setup
import re


def get_long_description():
    handle = open("README.txt")
    while not next(handle).startswith("====="):
        pass
    long_description = []
    for line in handle:
        if line.startswith("=====") or not line.strip():
            break
        line = re.sub(":[a-z]*:`([^`<]*[^`< ])[^`]*`", "\\1", line)
        long_description.append(line)
    return ''.join(long_description[:-1])

setup(
    name="backtask",
    description="Run functions in a background process",
    long_description=get_long_description(),
    version="backtask",
    author="Russell Stuart",
    author_email="russell-debian@stuart.id.au",
    url="http://backtask-py.sourceforge.net/",
    py_modules=["backtask"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
