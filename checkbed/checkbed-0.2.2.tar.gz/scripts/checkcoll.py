#!/usr/bin/env python3

import sys
from checkbed.Checkcoll import Checkcoll

helpmsg = """
Description:
Sample some SNPs out of each of the collapsed bed files, and check if they are correct

Usage:
checkcoll BED_FILE NCHECK_EACH

Commandline Arguments:
BED_FILE:           .bed file path (original, not the collapsed bed files)
NCHECK_EACH:        how many SNPs to check for each collapsed bed file?
"""

if "-h" in sys.argv or "--help" in sys.argv:
    print(helpmsg)
    exit(0)

x = Checkcoll(sys.argv[1])
if   len(sys.argv) == 3:
    if not sys.argv[2].isdigit():
        print(helpmsg)
        raise Exception("Wrong argument, NCHECK_EACH must be a positive integer!")
    x.checkall(int(sys.argv[2]))
elif len(sys.argv) == 2:
    x.checkall()
else:
    print(helpmsg)
    raise Exception("Arguments invalid!")
