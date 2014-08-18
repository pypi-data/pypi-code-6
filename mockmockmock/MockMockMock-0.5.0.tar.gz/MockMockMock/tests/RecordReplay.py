# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MockMockMock. http://jacquev6.github.com/MockMockMock

# MockMockMock is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MockMockMock is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MockMockMock.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import MockMockMock


# @todo Replace by a mock :-D
class TestDependency:
    theException = Exception("ga", "bu")

    def __init__(self):
        self.instanceProperty = 49

    classProperty = 48

    @property
    def propertyFromGetter(self):
        return 50

    @property
    def raisingProperty(self):
        raise self.theException

    def instanceMethod(self, x, y, *args, **kwds):
        return str((x, y, args, sorted(kwds.iteritems())))

    @classmethod
    def classMethod(cls, x, y):
        return (y, x, "foo")

    @staticmethod
    def staticMethod(x, y):
        return (y, x, "bar")

    def __call__(self, x, y):
        return (y, x, "baz")

    def raiseException(self, *args, **kwds):
        raise self.theException


class RecordTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.engine = MockMockMock.Engine()
        dependencyMock = self.engine.create("dependency")
        self.injectedDependency = dependencyMock.record(TestDependency())

    def testInstanceMethod(self):
        self.assertEqual(self.injectedDependency.instanceMethod(42, 43, 44, 45, toto=46, tutu=47), "(42, 43, (44, 45), [('toto', 46), ('tutu', 47)])")
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "instanceMethod",
                "arguments": (42, 43, 44, 45),
                "keywords": dict(toto=46, tutu=47),
                "return": "(42, 43, (44, 45), [('toto', 46), ('tutu', 47)])",
            }
        ])

    def testClassMethod(self):
        self.assertEqual(self.injectedDependency.classMethod(42, y=43), (43, 42, "foo"))
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "classMethod",
                "arguments": (42, ),
                "keywords": dict(y=43),
                "return": (43, 42, "foo"),
            }
        ])

    def testStaticMethod(self):
        self.assertEqual(self.injectedDependency.staticMethod(42, y=43), (43, 42, "bar"))
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "staticMethod",
                "arguments": (42, ),
                "keywords": dict(y=43),
                "return": (43, 42, "bar"),
            }
        ])

    def testCallObject(self):
        self.assertEqual(self.injectedDependency(42, y=43), (43, 42, "baz"))
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "__call__",
                "arguments": (42, ),
                "keywords": dict(y=43),
                "return": (43, 42, "baz"),
            }
        ])

    def testClassProperty(self):
        self.assertEqual(self.injectedDependency.classProperty, 48)
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "classProperty",
                "return": 48,
            }
        ])

    def testInstanceProperty(self):
        self.assertEqual(self.injectedDependency.instanceProperty, 49)
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "instanceProperty",
                "return": 49,
            }
        ])

    def testPropertyFromGetter(self):
        self.assertEqual(self.injectedDependency.propertyFromGetter, 50)
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "propertyFromGetter",
                "return": 50,
            }
        ])

    def testExceptionInMethod(self):
        with self.assertRaises(Exception) as cm:
            self.injectedDependency.raiseException(42, 43, z=45)
        self.assertIs(cm.exception, TestDependency.theException)
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "raiseException",
                "arguments": (42, 43),
                "keywords": {"z": 45},
                "exception": TestDependency.theException,
            }
        ])

    def testExceptionInProperty(self):
        with self.assertRaises(Exception) as cm:
            self.injectedDependency.raisingProperty
        self.assertIs(cm.exception, TestDependency.theException)
        self.engine.tearDown()
        self.assertEqual(self.engine.records, [
            {
                "object": "dependency",
                "attribute": "raisingProperty",
                "exception": TestDependency.theException,
            }
        ])
