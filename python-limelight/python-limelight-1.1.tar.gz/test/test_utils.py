# -*- coding: utf-8 -*-

from unittest import TestCase

from limelight.utils import to_camel_case, to_underscore, capitalize


class TestUtils(TestCase):
    def setUp(self):
        self.underscore_name = "make_sure_this_is_enough"
        self.camel_name = "makeSureThisIsEnough"
        self.initial_cap_underscore_name = "Make_sure_this_is_enough"
        self.initial_cap_camel_name = "MakeSureThisIsEnough"

    def test_to_camel_case(self):
        self.assertEqual(to_camel_case(self.underscore_name),
                         self.camel_name)
        self.assertEqual(to_camel_case(self.underscore_name, initial_cap=True),
                         self.initial_cap_camel_name)

    def test_to_underscore(self):
        self.assertEqual(to_underscore(self.camel_name), self.underscore_name)
        self.assertEqual(to_underscore(self.camel_name, initial_cap=True),
                         self.initial_cap_underscore_name)

    def test__initial_cap(self):
        self.assertEqual(capitalize(self.underscore_name), self.initial_cap_underscore_name)
        self.assertEqual(capitalize(self.camel_name), self.initial_cap_camel_name)
