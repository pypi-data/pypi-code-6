#!/usr/bin/python
# -*- coding: utf-8 -*-

# Code for NAO:
# input> string (sentence)
# output>string (joke)

import sys
from PyJoke.PyJoke import *

# user input
sentence = str(sys.argv[1])
pyjoke = PyJoke(sentence)
