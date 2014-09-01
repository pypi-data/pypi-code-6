#!/usr/bin/env python
"""
jboss.* scripts item

This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
Copyright (c) 2001 Wrike, Inc. [http://www.wrike.com]

Example usage:
    ./jboss.py get_prop jboss.system:type=ServerInfo FreeMemory
"""

from ztc.java.jboss import JMXJboss

j = JMXJboss()
m = j.args[0]
j.get(m, *j.args[1:])