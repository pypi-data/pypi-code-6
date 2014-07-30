#!/usr/bin/env python

import server.server

if __name__ == '__main__':
    print "Starting Server ..."
    s = server.server.Server(9000,9001)
    s.start()
