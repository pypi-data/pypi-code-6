#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_monster
------------

Tests for `box` module.
"""

import unittest
import json
import hashlib
from federated_monsters import monster


class MonsterTest(unittest.TestCase):

    """A unit test for the `box` module."""

    def test_export(self):
        ex_monster = monster.Monster("Smoke", "fluff", "normal", [])
        test_hash = hashlib.sha512(json.dumps(ex_monster.__dict__)
                                   .encode("utf-8"))
        actual_val = ex_monster.export_monster()[0]
        print(actual_val)

        self.assertEqual(actual_val, test_hash.hexdigest())
