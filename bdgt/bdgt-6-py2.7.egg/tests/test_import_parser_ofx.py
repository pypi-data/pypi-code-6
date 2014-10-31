import datetime
import os
import tempfile
from decimal import Decimal

from nose.tools import eq_, ok_

from bdgt.importer.parsers import OfxParser


def test_parse():
    ofx_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with ofx_file as f:
            f.write("""
            <OFX>
                <SIGNONMSGSRSV1>
                <SONRS>
                    <STATUS>
                    <CODE>0
                    <SEVERITY>INFO
                    </STATUS>
                    <DTSERVER>20071015021529.000[-8:PST]
                    <LANGUAGE>ENG
                    <DTACCTUP>19900101000000
                    <FI>
                    <ORG>MYBANK
                    <FID>01234
                    </FI>
                </SONRS>
                </SIGNONMSGSRSV1>
                <BANKMSGSRSV1>
                    <STMTTRNRS>
                    <TRNUID>23382938
                    <STATUS>
                        <CODE>0
                        <SEVERITY>INFO
                    </STATUS>
                    <STMTRS>
                        <CURDEF>USD
                        <BANKACCTFROM>
                        <BANKID>987654321
                        <ACCTID>098-121
                        <ACCTTYPE>SAVINGS
                        </BANKACCTFROM>
                        <BANKTRANLIST>
                        <DTSTART>20070101
                        <DTEND>20071015
                        <STMTTRN>
                            <TRNTYPE>CREDIT
                            <DTPOSTED>20070315
                            <DTUSER>20070315
                            <TRNAMT>200.00
                            <FITID>980315001
                            <NAME>DEPOSIT
                            <MEMO>description lines
                        </STMTTRN>
                        </BANKTRANLIST>
                        <LEDGERBAL>
                        <BALAMT>5250.00
                        <DTASOF>20071015021529.000[-8:PST]
                        </LEDGERBAL>
                        <AVAILBAL>
                        <BALAMT>5250.00
                        <DTASOF>20071015021529.000[-8:PST]
                        </AVAILBAL>
                    </STMTRS>
                    </STMTTRNRS>
                </BANKMSGSRSV1>
            </OFX>
            """)
        parser = OfxParser()
        txs = parser.parse(ofx_file.name)
        eq_(len(txs), 1)
        eq_(txs[0].parsed_tx.date, datetime.date(2007, 3, 15))
        eq_(txs[0].parsed_tx.account, '098-121')
        ok_('description lines' in txs[0].parsed_tx.description)
        eq_(txs[0].parsed_tx.amount, Decimal('200.00'))
    finally:
        os.remove(ofx_file.name)
