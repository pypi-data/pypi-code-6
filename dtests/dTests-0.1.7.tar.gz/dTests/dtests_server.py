#!/usr/bin/env python

import server.server

print "Starting Server ..."
s = server.server.Server(9000,9001)
s.start()
