import unittest
import datetime as dt

import datetools

class TestWindow(unittest.TestCase):
    def setUp(self):
        self.start = dt.datetime(2013, 1, 1, 0, 0, 0)
        self.middle = dt.datetime(2013, 1, 2, 0, 0, 0)
        self.end = dt.datetime(2013, 1, 3, 0, 0, 0)
        self.dates = [self.start, self.middle, self.end]

    def test_datewindow_lower_limit_inside_range(self):
        start = self.start
        end = self.middle
        index = datetools.datewindow(self.dates, start, end)
        expect = [self.start,]
        self.assertEqual(self.dates[index], expect)

    def test_datewindow_upper_limit_inside_range(self):
        start = self.middle
        end = self.end
        index = datetools.datewindow(self.dates, start, end)
        expect = [self.middle,]
        self.assertEqual(self.dates[index], expect)

    def test_datewindow_empty_list_returns_empty_list(self):
        dates = []
        start = self.start
        end = self.end
        index = datetools.datewindow(dates, start, end)
        expect = []
        self.assertEqual(dates[index], expect)

    def test_datewindow_include_end_point(self):
        start = self.start
        end = self.end
        index = datetools.datewindow(self.dates, start, end, 
                                     endpoint=True)
        expect = self.dates
        self.assertEqual(self.dates[index], expect)
