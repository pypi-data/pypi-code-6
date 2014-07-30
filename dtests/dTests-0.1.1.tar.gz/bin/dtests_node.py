#!/usr/bin/env python

import dTests.node.node

if __name__ == '__main__':
    print "Starting Node ..."
    node = dTests.node.node.Node(9000)
    node.start()
