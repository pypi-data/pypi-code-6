#!/usr/bin/env python

"""
make a string one line
"""

import sys
from .decorator import lines

@lines
def onelineit(string):
    """make a string one line"""

    string = [ i.strip() or '\n' for i in string ]
    string = ' '.join(string)
    string = string.split('\n')
    string = [ i.strip() for i in string if i.strip() ]

    return '\n\n'.join(string).splitlines()

def main(args=sys.argv[1:]):
    """CLI"""
    print (onelineit(sys.stdin.read()))

if __name__ == '__main__':
    main()
