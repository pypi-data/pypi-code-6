import unittest
import datetools

class TestShiftDate(unittest.TestCase):
    def test_shiftdate_move_date_forward_one_day(self):
        date = "20140101"
        days = 1
        result = datetools.shiftdate(date, days)
        expect = "20140102"
        self.assertEqual(expect, result)

    def test_shiftdate_move_date_backward_one_day(self):
        date = "20140101"
        days = -1
        result = datetools.shiftdate(date, days)
        expect = "20131231"
        self.assertEqual(expect, result)

    def test_shiftdate_given_custom_format_returns_formatted_output(self):
        date = "2014/01/01"
        days = 3
        fmt = "%Y/%m/%d"
        result = datetools.shiftdate(date, days, fmt=fmt)
        expect = "2014/01/04"
        self.assertEqual(expect, result)

    def test_shiftdate_given_custom_interval_returns_correct_string(self):
        date = "2014010100"
        days = 1
        fmt = "%Y%m%d%H"
        interval = datetools.HOUR
        result = datetools.shiftdate(date, days, fmt=fmt,
                                     interval=interval)
        expect = "2014010101"
        self.assertEqual(expect, result)

class TestShiftDates(unittest.TestCase):
    def test_shiftdates_shifts_lists_of_dates_forward_by_one_day(self):
        dates = ["20130101", "20130506"]
        days = 1
        result = datetools.shiftdates(dates, 1)
        expect = ["20130102", "20130507"]
        self.assertEqual(expect, result)
    def test_shiftdates_implements_custom_format_functionality(self):
        dates = ["2013-01-01", "2013-05-06"]
        days = 1
        fmt = "%Y-%m-%d"
        result = datetools.shiftdates(dates, 1, fmt=fmt)
        expect = ["2013-01-02", "2013-05-07"]
        self.assertEqual(expect, result)


