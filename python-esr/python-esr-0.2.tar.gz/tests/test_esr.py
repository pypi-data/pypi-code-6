import os
import unittest
from decimal import Decimal
from datetime import date

from esr import ESR, ESRRecordType3, ESRRecordType4, ESRValueError


class TestESR(unittest.TestCase):

    def setUp(self):
        with open(os.path.join('tests', 'data', 'esr_type3.v11')) as f:
            self.data_type3 = f.read()
        with open(os.path.join('tests', 'data', 'esr_type4.v11')) as f:
            self.data_type4 = f.read()

    def test_parse_esr_type3(self):
        e = ESR.parse(self.data_type3)
        self.assertEqual(len(e.records), 8)

        record = e.records[0]
        self.assertEqual(record.transaction_code, '002')
        self.assertEqual(record.customer_nr, '01-1067-4')
        self.assertEqual(record.reference, '52037000000000000000307249')
        self.assertEqual(record.amount, Decimal('500.0'))
        self.assertEqual(record.issue_date, date(2012, 11, 27))
        self.assertEqual(record.processing_date, date(2012, 11, 27))
        self.assertEqual(record.credit_date, date(2012, 11, 27))
        self.assertEqual(record.microfilm_nr, 0)
        self.assertEqual(record.reject_code, 0)
        self.assertEqual(record.price, Decimal('0.0'))

        record = e.total_record
        self.assertEqual(record.transaction_code, '999')
        self.assertEqual(record.customer_nr, '01-1067-4')
        self.assertEqual(record.amount, Decimal('13301.80'))
        self.assertEqual(record.transaction_count, 8)
        self.assertEqual(record.creation_date, date(2012, 12, 3))
        self.assertEqual(record.price, Decimal('0.0'))
        self.assertEqual(record.price_esr_plus, Decimal('0.0'))

    def test_parse_esr_type3_invalid_lines(self):
        # empty line
        line = ''
        self.assertRaises(ValueError, ESRRecordType3.parse, line)

        # nonsense line
        line = 'abcdefg'
        self.assertRaises(ValueError, ESRRecordType3.parse, line)

        # invalid transaction code
        line = '702' + '0' * 97
        self.assertRaises(ESRValueError, ESRRecordType3.parse, line)

        # missing information
        line = '002010010674'
        self.assertRaises(ValueError, ESRRecordType3.parse, line)

        # invalid date
        line = '002010010674' + '0' * 47 + '000000'
        self.assertRaises(ValueError, ESRRecordType3.parse, line)

        # invalid reject code
        line = ('002010010674' + '0' * 47 + '140101' * 3 + '0' * 9 + '7' +
                '0' * 13)
        self.assertRaises(ESRValueError, ESRRecordType3.parse, line)

    def test_parse_esr_type4(self):
        e = ESR.parse(self.data_type4)
        self.assertEqual(len(e.records), 8)

        record = e.records[0]
        self.assertEqual(record.transaction_code, '011')
        self.assertEqual(record.origin, 1)
        self.assertEqual(record.delivery_type, 1)
        self.assertEqual(record.customer_nr, '01-1067-4')
        self.assertEqual(record.reference, '52037000000000000000307249')
        self.assertEqual(record.amount_currency, 'CHF')
        self.assertEqual(record.amount, Decimal('500.0'))
        self.assertEqual(record.issue_date, date(2012, 11, 27))
        self.assertEqual(record.processing_date, date(2012, 11, 27))
        self.assertEqual(record.credit_date, date(2012, 11, 27))
        self.assertEqual(record.reject_code, 0)
        self.assertEqual(record.price_currency, 'CHF')
        self.assertEqual(record.price, Decimal('0.0'))

        record = e.total_record
        self.assertEqual(record.transaction_code, '991')
        self.assertEqual(record.origin, 99)
        self.assertEqual(record.delivery_type, 1)
        self.assertEqual(record.customer_nr, '01-1067-4')
        self.assertEqual(record.amount_currency, 'CHF')
        self.assertEqual(record.amount, Decimal('13301.80'))
        self.assertEqual(record.transaction_count, 8)
        self.assertEqual(record.creation_date, date(2012, 12, 3))
        self.assertEqual(record.price_currency, 'CHF')
        self.assertEqual(record.price, Decimal('0.0'))

    def test_parse_esr_type4_invalid_lines(self):
        # empty line
        line = ''
        self.assertRaises(ValueError, ESRRecordType4.parse, line)

        # nonsense line
        line = 'abcdefg'
        self.assertRaises(ValueError, ESRRecordType4.parse, line)

        # invalid transaction code
        line = '702' + '0' * 197
        self.assertRaises(ESRValueError, ESRRecordType4.parse, line)

        # missing information
        line = '002010010674'
        self.assertRaises(ValueError, ESRRecordType4.parse, line)

        # invalid date
        line = '002010010674' + '0' * 47 + '000000'
        self.assertRaises(ValueError, ESRRecordType4.parse, line)

        # invalid reject code
        line = ('011011010010674' + '0' * 27 + 'CHF' + '0' * 12 + ' ' * 35 +
                '20140101' * 3 + '7' + 'CHF' + '0' * 6 + ' ' * 74)
        self.assertRaises(ESRValueError, ESRRecordType4.parse, line)
