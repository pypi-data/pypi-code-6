# -*- coding: utf-8 -*-
"""
Anvil tests
"""

import os
import shutil
import tempfile
import unittest

from anvil import Anvil
from argparse import Namespace
# TODO: mocking

class AnvilTest(unittest.TestCase):
    
    def setUp(self):
        input_path = os.path.abspath('tests/example/input')
        output_path = os.path.abspath('tests/example')
        self.anvil = Anvil(input_path=input_path,
            output_path=output_path)
        self.target_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.target_dir)

    def test_render_file(self):
        intro = 'Example intro'
        self.anvil.render_file('{{project_name}}/README.rst', self.target_dir,
                               context={'intro': intro})
        render_file_path = os.path.join(self.target_dir, 'README.rst')
        self.assertTrue(os.path.isfile(render_file_path))
        with open(render_file_path, 'r') as f:
            self.assertTrue(intro in f.read())

        
if __name__ == "__main__":
    unittest.main()