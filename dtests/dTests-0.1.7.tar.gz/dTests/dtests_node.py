#!/usr/bin/env python

import node.node
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Create dTests node')
    
    parser.add_argument('--host', default='127.0.0.1',help='The server\'s host ip')
    parser.add_argument('--port', '-p', default=9000 ,help='The server\'s port')
    return parser

parser = create_parser()
args = parser.parse_args()
print "Starting Node ..."
node = node.node.Node(args.host,int(args.port))
node.start()
