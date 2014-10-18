import datetime
import os
import tempfile

from mock import patch
from nose.tools import eq_

from bdgt.importer.parsers import CsvIngParser


@patch('os.path.exists', return_value=True)
def test_parse(mock_exists):
    # TODO: mock either csv or open to return this data instead of using a
    #       tempfile. I did try this but couldn't get it working.

    txs_data = '"Datum","Naam / Omschrijving","Rekening","Tegenrekening","Code","Af Bij","Bedrag (EUR)","MutatieSoort","Mededelingen"\n' + \
               '"20150801","Naam en omsch.","987654321","11112222","BA","Af","12,75","Betaalautomaat","Mededelingen hier"\n' + \
               '"20150802","Naam en omsch.","987654321","12321232","GT","Bij","8,50","Internetbankieren","Mededelingen hier"'

    data_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with data_file as f:
            f.write(txs_data)

        parser = CsvIngParser()
        txs = parser.parse(data_file.name)

        eq_(len(txs), 2)
        eq_(txs[0]._parsed_tx.date, datetime.date(2015, 8, 1))
        eq_(txs[0]._parsed_tx.amount, -12.75)
        eq_(txs[0]._parsed_tx.account, '987654321')
        eq_(txs[0]._parsed_tx.description, 'Naam en omsch.')
        eq_(txs[1]._parsed_tx.date, datetime.date(2015, 8, 2))
        eq_(txs[1]._parsed_tx.amount, 8.50)
        eq_(txs[1]._parsed_tx.account, '987654321')
        eq_(txs[1]._parsed_tx.description, 'Naam en omsch.')
    finally:
        os.remove(data_file.name)
