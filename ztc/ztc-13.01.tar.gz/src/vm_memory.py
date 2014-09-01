#!/usr/bin/env python
"""
vm.memory.* scripts item


This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>

Params:
    $1 - metric name. Supported:
        active - amount of active (recently accessed) memory
        inavtive - amount of inactive (not accessed recently) memory
"""

import sys

from ztc.vm.memory import Memory
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

try:
    m = Memory()

    print m.__getattribute__(metric)
except Exception, e:
    notsupported(e)