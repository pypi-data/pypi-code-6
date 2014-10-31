#!/usr/bin/env python3

from checkbed.Checkcoll import Checkcoll
import sys

x = Checkcoll(sys.argv[1])
x.bedinfo()