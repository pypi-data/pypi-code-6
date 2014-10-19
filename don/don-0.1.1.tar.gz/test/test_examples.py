# Copyright (c) 2014 Susam Pal
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""Tests to verify examples in README.rst."""


import unittest
import don


class ExamplesTest(unittest.TestCase):

    def test_getting_started_example(self):
        s = """
        title: Countries

        india.capital: New Delhi
        india.demonym: Indian
        india.driving: Left

        italy.capital: Rome
        italy.demonym: Italian
        italy.driving: Right
        """

        # Parse DON
        root = don.parse(s)

        # Access a root attribute
        self.assertEqual(root.title, 'Countries')
        self.assertEqual(root.india.capital, 'New Delhi')
        self.assertEqual(root['india']['demonym'], 'Indian')
        self.assertEqual(root.india['driving'], 'Left')
        self.assertEqual(root.italy, {'driving': 'Right',
                                      'capital': 'Rome',
                                      'demonym': 'Italian'})

    def test_simple_example(self):
        s = """
        fruit: mango
        drink: beer
        level: debug
        """
        self.assertEqual(don.parse(s), {'fruit': 'mango',
                                        'drink': 'beer',
                                        'level': 'debug'})

    def test_blank_lines_and_comments(self):
        s = """
        # Eat and drink
        fruit: mango
        drink: beer

        # Logging level
        level: debug
        """
        self.assertEqual(don.parse(s), {'fruit': 'mango',
                                        'drink': 'beer',
                                        'level': 'debug'})

    def test_leading_and_trailing_whitespace(self):
        s = """
        # Eat and drink
          fruit : mango
            drink: beer

          # Logging level
        level:debug
        """
        self.assertEqual(don.parse(s), {'fruit': 'mango',
                                        'drink': 'beer',
                                        'level': 'debug'})

    def test_don_tree(self):
        s = """
        process.priority: normal
        process.protocol: tcp
        process.log.file: log.txt
        process.log.level: debug
        process.log.rotate: daily
        """
        root = don.parse(s)
        self.assertEqual(root, {'process': {'priority': 'normal',
                                            'protocol': 'tcp',
                                            'log': {'file': 'log.txt',
                                                    'level': 'debug' ,
                                                    'rotate': 'daily'}}})
        self.assertIs(type(root), don.Object)
        self.assertIs(type(root.process), don.Object)
        self.assertIs(type(root.process.priority), str)
        self.assertIs(type(root.process.protocol), str)
        self.assertIs(type(root.process.log), don.Object)
        self.assertIs(type(root.process.log.file), str)
        self.assertIs(type(root.process.log.level), str)
        self.assertIs(type(root.process.log.rotate), str)

    def test_empty_values(self):
        s = """
        process.priority: normal
        .protocol: tcp
        .log.file: log.txt
        ..level: debug
        ..rotate: daily
        """
        root = don.parse(s)
        self.assertEqual(root, {'process': {'priority': 'normal',
                                            'protocol': 'tcp',
                                            'log': {'file': 'log.txt',
                                                    'level': 'debug' ,
                                                    'rotate': 'daily'}}})

    def test_empty_values_with_identation(self):
        s = """
        process.priority: normal
               .protocol: tcp 
               .log.file: log.txt
                  ..level: debug
                  ..rotate: daily
        """
        root = don.parse(s)
        self.assertEqual(root, {'process': {'priority': 'normal',
                                            'protocol': 'tcp',
                                            'log': {'file': 'log.txt',
                                                    'level': 'debug' ,
                                                    'rotate': 'daily'}}})

    def test_declaration(self):
        s = """
        process:
            .priority: normal
            .protocol: tcp 
            .log:
                ..file: log.txt
                ..level: debug
                ..rotate: daily
        """
        root = don.parse(s)
        self.assertEqual(root, {'process': {'priority': 'normal',
                                            'protocol': 'tcp',
                                            'log': {'file': 'log.txt',
                                                    'level': 'debug' ,
                                                    'rotate': 'daily'}}})
