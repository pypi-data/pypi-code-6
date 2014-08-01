# -*- coding: utf-8 -*-

import os
import random
import sys


__DATA_PATH = os.path.dirname(os.path.realpath(__file__))

def main():
    """
    Main

    """
    # Read monty_python.txt
    with open(__DATA_PATH + '/monty_python.txt', 'r') as f:
        monty_python = f.readlines()

    sys.stdout.write("%s\n" % (random.choice(monty_python).strip()))

if '__main__' == __name__:
    main()
