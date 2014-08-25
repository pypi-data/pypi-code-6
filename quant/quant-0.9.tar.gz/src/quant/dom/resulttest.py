from quant.dom.testunit import TestCase
import unittest
import datetime

def suite():
    suites = [
        unittest.makeSuite(TestResult),
    ]
    return unittest.TestSuite(suites)

class TestResult(TestCase):

    now = datetime.datetime.now()
    thisYear = now.year
    thisMonth = now.month
    thisDay = now.day
    observationTime = datetime.datetime(thisYear, thisMonth, thisDay)

    def setUp(self):
        self.image = self.registry.images.findDomainObjects()[-1]
        self.book = self.registry.books.values()[0]
        self.failUnlessEqual(self.book.title, "My Book")
        self.result = self.registry.results.create(book=self.book, image=self.image)

    def tearDown(self):
        self.result.delete()

    def test_result(self):
        self.assertTrue(self.result)
        self.assertTrue(len(self.result.lines))

