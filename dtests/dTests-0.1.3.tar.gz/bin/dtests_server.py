#!/usr/bin/env python

import dTests.server.server

if __name__ == '__main__':
    print "Starting Server ..."
    s = dTests.server.server.Server(9000,9001)
    s.start()
