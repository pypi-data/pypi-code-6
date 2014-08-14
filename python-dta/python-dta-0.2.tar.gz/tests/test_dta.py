import unittest
from datetime import date
from decimal import Decimal

from dta import DTA
from dta.records import DTAHeader, DTARecord826, DTARecord827, DTARecord890


class TestDTA(unittest.TestCase):

    def test_generate_dta(self):
        dta = DTA()

        header = self._get_header()
        header.sequence_nr = 1
        header.processing_date = date(2013, 5, 10)
        header.recipient_clearing_nr = '81487'

        record = DTARecord827(header)
        record = self._set_common_fields(record)
        record.reference = '002013-0059'
        record.amount = Decimal('1500.00')
        record.recipient_account = '69444.84'
        record.recipient_address1 = 'TESTLIEFERANT 1'
        record.recipient_address3 = 'POSTFACH 2322'
        record.recipient_address4 = '8033 ZUERICH'
        dta.records.append(record)

        header = self._get_header()
        header.sequence_nr = 2
        header.processing_date = date(2013, 5, 10)

        record = DTARecord826(header)
        record = self._set_common_fields(record)
        record.reference = '002013-0058'
        record.amount = Decimal('114.35')
        record.esr_reference = '182171015574297'
        record.recipient_account = '010723327'
        record.recipient_address1 = 'TESTLIEFERANT 2'
        record.recipient_address3 = 'LANDENBERSTRASSE 21'
        record.recipient_address4 = '6002 LUZERN'
        dta.records.append(record)

        header = self._get_header()
        header.sequence_nr = 3
        header.processing_date = date(2013, 5, 10)

        record = DTARecord826(header)
        record = self._set_common_fields(record)
        record.reference = '002013-0057'
        record.amount = Decimal('5.00')
        record.esr_reference = '1005709899004994220520128'
        record.recipient_account = '010231043'
        record.recipient_address1 = 'TESTLIEFERANT 3'
        record.recipient_address3 = 'TIEFENAUSTRASSE 10'
        record.recipient_address4 = '3050 BERN'
        dta.records.append(record)

        header = self._get_header()
        header.sequence_nr = 4
        header.processing_date = date(2013, 5, 10)

        record = DTARecord826(header)
        record = self._set_common_fields(record)
        record.reference = '002013-0056'
        record.amount = Decimal('566.55')
        record.esr_reference = '100006561217201100020201122'
        record.recipient_account = '010541840'
        record.recipient_address1 = 'TESTLIEFERANT 4'
        record.recipient_address3 = 'ARSENALSTRASSE 52'
        record.recipient_address4 = '6010 KRIENS'
        dta.records.append(record)

        header = self._get_header()
        header.sequence_nr = 5
        header.processing_date = date(2013, 5, 10)

        record = DTARecord826(header)
        record = self._set_common_fields(record)
        record.reference = '002013-0055'
        record.amount = Decimal('14.00')
        record.esr_reference = '1005709899005605610720128'
        record.recipient_account = '010231043'
        record.recipient_address1 = 'TESTLIEFERANT 3'
        record.recipient_address3 = 'TIEFENAUSTRASSE 10'
        record.recipient_address4 = '3050 BERN'
        dta.records.append(record)

        header = self._get_header()
        header.sequence_nr = 6

        record = DTARecord890(header)
        record.amount = Decimal('2199.90')
        dta.records.append(record)

        output = dta.generate()
        self.assertEqual(len(output), 2080)

    def _get_header(self):
        header = DTAHeader()
        header.sender_id = 'ABCDE'
        header.client_clearing_nr = '248'
        header.creation_date = date(2013, 4, 23)
        return header

    def _set_common_fields(self, record):
        record.currency = 'CHF'
        record.liability_account = '248 110079.01Z'
        record.client_address1 = 'LEUCHTER OPEN SOURCE SOLUTIONS'
        record.client_address3 = 'WINKELRIEDSTRASSE 45'
        record.client_address4 = '6003 LUZERN'
        return record
