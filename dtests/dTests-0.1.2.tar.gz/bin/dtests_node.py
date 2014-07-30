#!/usr/bin/env python

import dTests.node.node
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Create dTests node')
    
    parser.add_argument('--host', default='127.0.0.1', nargs=1,help='The server\'s host ip')
    parser.add_argument('--port', '-p', default=9000, nargs=1,help='The server\'s port')
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    print "Starting Node ..."
    print args.port
    node = dTests.node.node.Node(args.host,args.port)
    node.start()
