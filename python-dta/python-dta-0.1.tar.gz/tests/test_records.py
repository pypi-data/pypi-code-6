import unittest
from datetime import date
from decimal import Decimal

from dta.records import DTAHeader, DTARecord826, DTARecord827, DTARecord836, \
    DTARecord890


class TestRecords(unittest.TestCase):

    def test_header(self):
        header = self._get_header()
        header.transaction_code = 826
        header.processing_date = date(2013, 05, 10)
        header.check()

        self.assertEqual(header.processing_date, '130510')
        self.assertEqual(header.recipient_clearing_nr, '            ')
        self.assertEqual(header.creation_date, '130423')
        self.assertEqual(header.client_clearing_nr, '248    ')
        self.assertEqual(header.sender_id, 'ABCDE')
        self.assertEqual(header.sequence_nr, '00001')
        self.assertEqual(header.transaction_code, '826')
        self.assertEqual(header.payment_type, '0')

        self.assertEqual(len(header.generate()), 51)

    def test_record826(self):
        header = self._get_header()
        header.processing_date = date(2013, 05, 10)

        record = DTARecord826(header)
        record.reference = '002013-0058'
        record.liability_account = '248 110079.01Z'
        record.currency = 'CHF'
        record.amount = Decimal('114.35')

        record.client_address1 = 'LEUCHTER OPEN SOURCE'
        record.client_address2 = ''
        record.client_address3 = 'WINKELRIEDSTRASSE 45'
        record.client_address4 = '6003 LUZERN'

        record.recipient_account = '010723327'
        record.recipient_address1 = 'TESTLIEFERANT 2'
        record.recipient_address2 = ''
        record.recipient_address3 = 'LANDENBERSTRASSE 21'
        record.recipient_address4 = '6002 LUZERN'
        record.esr_reference = '182171015574297'

        self.assertEqual(record.amount, '114,35      ')
        self.assertEqual(len(record.generate()), 388)

    def test_record827(self):
        header = self._get_header()
        header.processing_date = date(2013, 05, 10)
        header.recipient_clearing_nr = '81487'

        record = DTARecord827(header)
        record.reference = '002013-0059'
        record.liability_account = '248 110079.01Z'
        record.currency = 'CHF'
        record.amount = Decimal('1500.00')

        record.client_address1 = 'LEUCHTER OPEN SOURCE SOL'
        record.client_address2 = ''
        record.client_address3 = 'WINKELRIEDSTRASSE 45'
        record.client_address4 = '6003 LUZERN'

        record.recipient_account = '69444.84'
        record.recipient_address1 = 'TESTLIEFERANT 1'
        record.recipient_address2 = ''
        record.recipient_address3 = 'POSTFACH 2322'
        record.recipient_address4 = '8033 ZUERICH'

        self.assertEqual(len(record.generate()), 388)

        record.message1 = 'Test'
        self.assertEqual(len(record.generate()), 518)

        record.beneficiary_account = '1234'
        self.assertEqual(len(record.generate()), 648)

    def test_record836(self):
        header = self._get_header()

        record = DTARecord836(header)
        record.reference = '002013-0059'
        record.liability_account = '248 110079.01Z'
        record.valuta = date(2013, 05, 10)
        record.currency = 'EUR'
        record.amount = Decimal('99.99')

        record.client_address1 = 'LEUCHTER OPEN SOURCE SOLUTIONS'
        record.client_address2 = 'WINKELRIEDSTRASSE 45'
        record.client_address3 = '6003 LUZERN'

        record.bank_address_type = 'D'
        record.recipient_iban = 'CH0509000000305927095'

        record.recipient_address1 = 'HANS MULLER'
        record.recipient_address2 = 'TESTSTRASSE 10'
        record.recipient_address3 = '6005 LUZERN'

        record.payment_reason_type = 'U'
        record.payment_reason1 = 'Lorem ipsum'
        record.charges_handling = 0

        self.assertEqual(len(record.generate()), 648)

    def test_record890(self):
        header = self._get_header()

        record = DTARecord890(header)
        record.amount = Decimal('999.99')

        self.assertEqual(len(record.generate()), 128)

    def _get_header(self):
        header = DTAHeader()
        header.recipient_clearing_nr = ''
        header.creation_date = date(2013, 04, 23)
        header.client_clearing_nr = '248'
        header.sender_id = 'ABCDE'
        header.sequence_nr = 1
        return header
