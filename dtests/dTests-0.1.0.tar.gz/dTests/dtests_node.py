#!/usr/bin/env python

import node.node

if __name__ == '__main__':
    print "Starting Node ..."
    node = node.node.Node(9000)
    node.start()
