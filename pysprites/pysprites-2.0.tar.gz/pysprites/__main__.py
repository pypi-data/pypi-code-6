#!/usr/bin/env python

if __name__ == '__main__' :
   import sys
   from pysprites import sprites, parse_argv
   sprites(**parse_argv(sys.argv))
