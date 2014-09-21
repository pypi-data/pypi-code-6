import unittest
import datetime as dt

import datetools

class TestDateRange(unittest.TestCase):
    def test_daterange_given_single_date_returns_list_with_same_date(self):
        start = "20130101"
        result = datetools.daterange(start)
        expect = [start,]
        self.assertEqual(expect, result)

    def test_daterange_given_end_date_returns_multiple_dates(self):
        start = "20130101"
        middle = "20130102"
        end = "20130103"
        result = datetools.daterange(start, end)
        expect = [start, middle, end]
        self.assertEqual(expect, result)

    def test_daterange_given_datetime_format_string_format_output(self):
        start = "2013-01-01"
        middle = "2013-01-02"
        end = "2013-01-03"
        fmt = "%Y-%m-%d"
        result = datetools.daterange(start, end, fmt=fmt)
        expect = [start, middle, end]
        self.assertEqual(expect, result)

    def test_daterange_given_reversed_dates_returns_empty_list(self):
        start = "20150101"
        end = "20140101"
        result = datetools.daterange(start, end)
        expect = []
        self.assertEqual(expect, result)

    def test_daterange_given_custom_interval_two_days(self):
        start = "20130101"
        middle = "20130103"
        end = "20130105"
        interval = dt.timedelta(days=2)
        result = datetools.daterange(start, end, interval=interval)
        expect = [start, middle, end]
        self.assertEqual(expect, result)

    def test_daterange_given_custom_interval_one_hour(self):
        start = "2013/01/01 00:00:00"
        middle = "2013/01/01 01:00:00"
        end = "2013/01/01 02:00:00"
        interval = dt.timedelta(seconds=60*60)
        fmt = "%Y/%m/%d %H:%M:%S"
        result = datetools.daterange(start, end, fmt=fmt,
                                     interval=interval)
        expect = [start, middle, end]
        self.assertEqual(expect, result)

    def test_daterange_given_number_of_intervals(self):
        start = "20140609"
        middle = "20140610"
        end = "20140611"
        numdates = 3
        result = datetools.daterange(start, numdates=numdates)
        expect = [start, middle, end]
        self.assertEqual(expect, result)

    def test_daterange_given_hourly_format_and_numdates(self):
        numdates = 3
        fmt = "%Y%m%d%H"
        start = "2014010100"
        result = datetools.daterange(start, numdates=numdates, fmt=fmt)
        expect = ["2014010100", "2014010200", "2014010300"]
        self.assertEqual(expect, result)

    def test_daterange_given_hourly_format_and_hourly_interval(self):
        numdates = 3
        fmt = "%Y%m%d%H"
        start = "2014010100"
        result = datetools.daterange(start, numdates=numdates, fmt=fmt,
                                     interval=datetools.HOUR)
        expect = ["2014010100", "2014010101", "2014010102"]
        self.assertEqual(expect, result)

    def test_daterange_given_flag_returns_datetime_objects(self):
        start = "20140620"
        expect = [dt.datetime(2014, 6, 20)]
        result = datetools.daterange(start, todatetime=True)
        self.assertEqual(expect, result)

    def test_daterange_given_datetime_objects(self):
        start = dt.datetime(2014, 6, 20)
        end = dt.datetime(2014, 6, 21)
        result = datetools.daterange(start, end)
        expect = ["20140620", "20140621"]
        self.assertEqual(expect, result)

