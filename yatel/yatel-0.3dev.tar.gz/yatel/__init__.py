#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

u"""Yatel allows the creation of user-profile-distance-based of OLAP Network
and their multidimensional analysis through a process of exploration.

In the process of analyzing data from heterogeneous sources - like
data regarding biology, social studies, marketing, etc. -, it is
often possible to identify individuals or classes (groups of
individuals that share some characteristic). This individuals or
groups are identified by attributes that were measured and stored in
the data data base. For instance, in a biological analysis, the
profile can be defined by some certain properties of the nucleic
acid, in a social  analysis by the data from people and in a sales
analysis by the data from sales point tickets.

"""


#===============================================================================
# IMPORTS
#===============================================================================

import encodings
import os
import sys


#===============================================================================
# CONSTANTS
#===============================================================================

# : This is the project name
PRJ = "Yatel"

# : The project version as tuple of strings
VERSION = ("0", "3dev")

# : The project version as string
STR_VERSION = ".".join(VERSION)
__version__ = STR_VERSION

# : For "what" is usefull yatel
DOC = __doc__

# : The short description for pypi
SHORT_DESCRIPTION = []
for line in DOC.splitlines():
    if not line.strip():
        break
    SHORT_DESCRIPTION.append(line)
SHORT_DESCRIPTION = u" ".join(SHORT_DESCRIPTION)
del line


# : Clasifiers for optimize search in pypi
CLASSIFIERS = (
    "Topic :: Utilities",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 2",
)

# : Home Page of yatel
URL = "http://getyatel.org"

# : Url of the official yatel doc
DOC_URL = "http://yatel.readthedocs.org"

# : Author of this yatel
AUTHOR = "Yatel Team"

# : Email ot the autor
EMAIL = "utn_kdd@googlegroups.com"

# : The license name
LICENSE = "WISKEY-WARE"

# : The license of yatel
FULL_LICENSE = u""""THE WISKEY-WARE LICENSE":
<utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
you can do whatever you want with this stuff. If we meet some day, and you
think this stuff is worth it, you can buy us a WISKEY in return.

"""

# : Keywords for search of pypi
KEYWORDS = """Yatel user-profile-distance-based networks  multidimensional
exploration database kdd datamining"""

# : If the program is en debug mode
DEBUG = __debug__


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
