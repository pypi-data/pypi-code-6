#!/usr/bin/env python
"""
terracotta.* scripts item

This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

from ztc.java.jmx import JMXCheck

j = JMXCheck()
m = j.args[0]
j.get(m, *j.args[1:])