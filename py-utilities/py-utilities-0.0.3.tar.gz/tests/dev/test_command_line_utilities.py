#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from nose.tools import raises
from py_utilities.dev.command_line_utilities import piped
from py_utilities.dev.command_line_utilities import prompt_yes_no
import sys
import tempfile
import unittest


bad_input = lambda x: 'foobar'
empty_input = lambda x: ''
fake_y = lambda x: 'y'
fake_capital_y = lambda x: 'Y'
fake_ye = lambda x: 'ye'
fake_yes = lambda x: 'yes'
fake_1 = lambda x: '1'
fake_n = lambda x: 'n'
fake_capital_n = lambda x: 'N'
fake_no = lambda x: 'no'
fake_0 = lambda x: '0'


class TestCommandLineUtilities(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.TemporaryFile()

    def test_piped_on_file(self):
        ok_(piped(self.temp_file) is not None)

    def test_piped_on_tty(self):
        ok_(piped(sys.stdin) is None)

    def test_prompt_yes_no_with_empty_input_and_defaults(self):
        yes = prompt_yes_no("Do you like green eggs and ham",
                            'yes', 5, empty_input)
        ok_(yes is True)
        no = prompt_yes_no("Do you like green eggs and ham",
                           'no', 5, empty_input)
        ok_(no is False)

    def test_prompt_yes_no_with_yes_input(self):
        yes_inputs = [fake_y, fake_capital_y, fake_ye, fake_yes, fake_1]
        for input in yes_inputs:
            yes = prompt_yes_no("Do you like green eggs and ham",
                                None, 5, input)

            ok_(yes is True)

    def test_prompt_yes_no_with_no_input(self):
        no_inputs = [fake_n, fake_capital_n, fake_no, fake_0]
        for input in no_inputs:
            no = prompt_yes_no("Do you like green eggs and ham",
                               None, 5, input)

            ok_(no is False)

    @raises(IOError)
    def test_prompt_yes_no_with_bad_input(self):
        prompt_yes_no("Do you like green eggs and ham", None, 5, bad_input)

    @raises(ValueError)
    def test_prompt_yes_no_with_bad_default(self):
        prompt_yes_no("Do you like green eggs and ham", 'foo', 5, bad_input)

# vim: filetype=python
