#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_box
--------

Tests for `box` module.
"""

import unittest
import operator
import json
from federated_monsters import box
from federated_monsters import db
from federated_monsters import monster


class BoxTest(unittest.TestCase):

    """A unit test for the `box` module."""

    def test_respond(self):
        test_box = box.Box()
        test_box.db = db.DB()
        out = [""]
        ex_monster = monster.Monster("Smoke", "fluff", "normal", [])
        exp = json.dumps(ex_monster.export_monster())

        cases = (
            ("hello world", "403 BAD_COMMAND hello"),
            ("HELLO WORLD", "403 BAD_COMMAND hello"),
            ("/echo hello world", "200 OK hello world"),
            ("/uploadmonster %s" % exp, "200 OK"))

        # Override the print_stream method so the test can use it.
        # Uses operator.setitem to get around inability to use assignments.
        test_box.print_stream = lambda y, z: operator.setitem(out, 0, z)
        # test_box.respond_to_input(None, "hello world")
        for sent, response in cases:
            test_box.respond_to_input(None, sent)
            self.assertEqual(out[0], response)
