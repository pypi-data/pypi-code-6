#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_box
--------

Tests for ``box`` module.
"""

import json
import operator
import os
import unittest

from federated_monsters import box, monster


# from federated_monsters import berkeley_db


class BoxTest(unittest.TestCase):

    """A unit test for the ``box`` module."""

    def test_respond(self):
        test_box = box.Box(db_fn="test.db")
        test_box.db.open_db()
        # test_box.db = berkeley_db.BerkeleyDB("test.db")
        out = [""]
        ex_monster = monster.Monster("Smoke", "fluff", "normal", [])
        exp = json.dumps(ex_monster.export_monster())
        exp_enc = json.dumps(ex_monster.export_monster(pwd=">install gentoo"))

        cases = (
            ("/uploadmonster %s" % exp, "200 OK"),
            ("/uploadmonster %s" % exp_enc, "200 OK"),
            ("hello world", "403 BAD_COMMAND hello"),
            ("HELLO WORLD", "403 BAD_COMMAND hello"),
            ("/echo hello world", "200 OK hello world"))

        # Override the print_stream method so the test can use it.
        # Uses operator.setitem to get around inability to use assignments.
        test_box.print_stream = lambda y, z: operator.setitem(out, 0, z)
        # test_box.respond_to_input(None, "hello world")
        for sent, response in cases:
            # print(sent)
            test_box.respond_to_input(None, sent)
            self.assertEqual(out[0].strip(), response)
        # test_box.db.close()
        os.remove("test.db")
