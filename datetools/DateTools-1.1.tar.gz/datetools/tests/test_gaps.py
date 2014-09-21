# pylint: disable=C0111
# pylint: disable=C0103
import unittest
import datetools


class TestGaps(unittest.TestCase):
    def test_gaps_given_single_missing_date_returns_list_containing_date(self):
        dates = ["20140101", "20140103"]
        result = datetools.gaps(dates)
        expect = ["20140102"]
        self.assertEqual(result, expect)

    def test_gaps_given_empty_list_returns_empty_list(self):
        dates = []
        result = datetools.gaps(dates)
        expect = []
        self.assertEqual(result, expect)

    def test_gaps_given_single_date_returns_empty_list(self):
        dates = ["20140606"]
        result = datetools.gaps(dates)
        expect = []
        self.assertEqual(result, expect)

    def test_gaps_given_multiple_dates_with_no_gaps_returns_empty_list(self):
        dates = ["20140606", "20140607", "20140608"]
        result = datetools.gaps(dates)
        expect = []
        self.assertEqual(result, expect)

    def test_gaps_given_unordered_dates_returns_missing_dates(self):
        dates = ["20140103", "20140101"]
        result = datetools.gaps(dates)
        expect = ["20140102"]
        self.assertEqual(result, expect)
