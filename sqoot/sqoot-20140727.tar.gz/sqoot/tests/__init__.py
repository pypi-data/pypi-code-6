#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal

import os, sys
import unittest

import sqoot

if 'PUBLIC_API_KEY' in os.environ and 'PRIVATE_API_KEY' in os.environ:
    PUBLIC_API_KEY = os.environ['PUBLIC_API_KEY']
    PRIVATE_API_KEY = os.environ['PRIVATE_API_KEY']
else:
    try:
        from _creds import *

    except ImportError:
        print "Please create a creds.py file in this package, based upon creds.example.py"


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'testdata')
sys.path.append('/home/ragarwal/sqoot')


class BaseEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.api = sqoot.Sqoot(
            privateApiKey=PRIVATE_API_KEY,
            publicApiKey=PUBLIC_API_KEY,
        )
