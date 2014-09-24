# coding: utf-8
"""
File: test_license.py
Author: Rinat F Sabitov
Description:
"""

import os
import unittest
from m3_license import api
import tempfile

from .env import LICENSE, PUBLIC_KEY

class GetDataTest(unittest.TestCase):

    def setUp(self):
        tmp_file, self.tmp_filename = tempfile.mkstemp()
        with os.fdopen(tmp_file, 'w') as f:
            f.write(LICENSE)


    def test_read_write(self):
        api.get_lic_data(self.tmp_filename, PUBLIC_KEY)
