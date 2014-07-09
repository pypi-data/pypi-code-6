#!/usr/bin/env python

"""
make a python module directory with an __init__.py
"""

import argparse
import os
import sys

def main(args=sys.argv[1:]):
    """CLI"""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory')
    options = parser.parse_args(args)

    os.makedirs(options.directory)
    init = os.path.join(options.directory, '__init__.py')
    with open(init, 'w') as f:
        f.write('#\n')

if __name__ == '__main__':
    main()
