import unittest
from quant.dom.testunit import TestCase
import datetime

def suite():
    suites = [
        unittest.makeSuite(BookTestCase)
    ]
    return unittest.TestSuite(suites)


class BookTestCase(TestCase):

    def setUp(self):
        self.book = self.registry.books.values()[0]
        self.failUnlessEqual(self.book.title, "My Book")

    def test_book(self):
        self.assertTrue(self.book)
        self.assertTrue(len(self.book.getContracts()))

