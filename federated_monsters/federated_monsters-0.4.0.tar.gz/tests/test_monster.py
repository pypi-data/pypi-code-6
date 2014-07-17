#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_monster
------------

Tests for ``monster`` module.
"""

import hashlib
import json
import unittest
import binascii

from federated_monsters import monster
from federated_monsters import crypto


class MonsterTest(unittest.TestCase):

    """A unit test for the ``monster`` module."""

    def test_export(self):
        ex_monster = monster.Monster("Smoke", "fluff", "normal", [])
        test_hash = hashlib.sha512(json.dumps(ex_monster.__dict__)
                                   .encode("utf-8"))
        actual_val = ex_monster.export_monster()[0]
        # print(actual_val)

        self.assertEqual(actual_val, test_hash.hexdigest())

    def test_encrypt(self):
        ex_monster = monster.Monster("Smoke", "fluff", "normal", [])
        exp_cry = ex_monster.export_monster(pwd=">implying implications")
        exp = ex_monster.export_monster()

        splt = exp_cry[1].split(" ")
        print("splt", splt[1].encode("UTF-8"))

        salt = crypto.hex_to_byte(splt[1].encode("UTF-8"))
        # print(salt)

        key = crypto.gen_key(">implying implications", salt)

        self.assertEqual(exp[1], crypto.decrypt(crypto.hex_to_byte(
                                                splt[0].encode("UTF-8")),
                                                key.key))
