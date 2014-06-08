#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from py_utilities.mixins.equality import EqualityMixin
import unittest


class Foo(EqualityMixin):
    def __init__(self, item):
        self.item = item


class SubclassFoo(Foo):
    pass


class TestEqualityMixin(unittest.TestCase):

    def test_equality_same_class(self):
        foo1 = Foo(1)
        foo2 = Foo(1)
        ok_((foo1 is foo2) is False)
        ok_(foo1 == foo2)
        ok_(foo2 == foo1)

    def test_equality_subclass_should_not_be_equal_or_not_equal(self):
        foo2 = Foo(1)
        foo3 = SubclassFoo(1)
        ok_((foo2 != foo3) is False)
        ok_((foo3 != foo2) is False)
        ok_((foo2 == foo3) is False)
        ok_((foo3 == foo2) is False)

# vim: filetype=python
