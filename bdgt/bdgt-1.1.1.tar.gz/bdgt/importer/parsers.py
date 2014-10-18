from __future__ import absolute_import

import datetime
import csv
import os
import re
import tempfile

from mt940 import MT940
from ofxparse import OfxParser as OfxLibParser

from bdgt.importer.types import ImportTx, ParsedTx


class TxParserFactory(object):
    @classmethod
    def create(cls, type_):
        if type_ == 'csv-ing':
            return CsvIngParser()
        elif type_ == 'mt940':
            return Mt940Parser()
        elif type_ == 'ofx':
            return OfxParser()
        else:
            raise ValueError("Unknown parser type '{}'".format(type_))


class Mt940Parser(object):
    def parse(self, file_):
        mt940 = MT940(file_)
        i_txs = []
        for f_stmt in mt940.statements:
            for f_tx in f_stmt.transactions:
                p_tx = ParsedTx(f_tx.booking, f_tx.amount,
                                unicode(f_tx.account),
                                unicode(f_tx.description))
                i_tx = ImportTx(p_tx)
                i_txs.append(i_tx)
        return i_txs


class OfxParser(object):
    def parse(self, file_):
        # ofxparse workaround
        # ofxparse doesn't parse the transaction amount correctly. It assumes
        # that the decimal point separator is always a full-stop; however, it
        # depends on the locale of the statement.
        #
        # This workaround finds the transaction amount in the file and replaces
        # comma with a full-stop. A temporary file is used to make the change
        # so the original file data stays intact.
        with open(file_) as f:
            data = f.read()
        data = re.sub(r'<TRNAMT>([-\d]+),([\d]+)', r'<TRNAMT>\1.\2', data)

        ofx_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            with ofx_file as f:
                f.write(data)

            # Actual parsing
            ofx = OfxLibParser.parse(file(ofx_file.name))
            i_txs = []
            for f_acc in ofx.accounts:
                for f_tx in f_acc.statement.transactions:
                    p_tx = ParsedTx(f_tx.date.date(), f_tx.amount,
                                    unicode(f_acc.number),
                                    unicode(f_tx.memo))
                    i_tx = ImportTx(p_tx)
                    i_txs.append(i_tx)
            return i_txs
        finally:
            os.remove(ofx_file.name)


class CsvIngParser(object):
    def parse(self, file_):
        if not os.path.exists(file_):
            raise ValueError("'{}' not found".format(file_))

        with open(file_, 'r') as f:
            csv_reader = csv.DictReader(f)
            i_txs = []
            for tx in csv_reader:
                # Parse the date. There are two formats: yyyymmdd and
                # dd-mm-yyyy.
                if '-' in tx['Datum']:
                    fmt = '%d-%m-%Y'
                else:
                    fmt = '%Y%m%d'
                tx_date = datetime.datetime.strptime(tx['Datum'], fmt).date()

                # Parse the amount. First assume that the decimal separator is
                # a '.'; otherwise, use ','.
                try:
                    tx_amount = float(tx['Bedrag (EUR)'])
                except ValueError:
                    tx_amount = float(tx['Bedrag (EUR)'].replace(',', '.'))
                if tx['Af Bij'] == 'Af':
                    tx_amount = -tx_amount

                tx_account = tx['Rekening']
                tx_description = tx['Naam / Omschrijving']

                p_tx = ParsedTx(tx_date, tx_amount, tx_account, tx_description)
                i_tx = ImportTx(p_tx)
                i_txs.append(i_tx)
            return i_txs
