import datetime
from decimal import Decimal
from StringIO import StringIO

import yaml
from mock import Mock, mock_open, patch
from nose.tools import eq_

from bdgt.commands.importer import CmdImport
from bdgt.importer.types import ImportTx, ParsedTx


@patch('bdgt.importer.parsers.TxParserFactory.create')
@patch('bdgt.commands.importer.open', mock_open(), create=True)
@patch('os.path.exists', return_value=False)
def test_cmd_import(mock_exists, mock_parser_factory):
    mock_parser = Mock()
    mock_parser_factory.return_value = mock_parser
    mock_parser.parse.return_value = [
        ImportTx(ParsedTx(datetime.date(2014, 11, 30),
                          Decimal('193.45'),
                          u"987654321",
                          u"desc"))]

    output = CmdImport("mt940", "data.dat", False)()

    eq_(output, "Parsed 1 transactions from data.dat.")


def test_cmd_import_save_parsed_txs():
    p_tx = ParsedTx(datetime.date(2014, 11, 30), Decimal('193.45'),
                    u"987654321", u"desc")
    txs = [ImportTx(p_tx)]
    import_file = StringIO()
    CmdImport._save_parsed_txs(txs, import_file)

    txs = yaml.load(import_file.getvalue())
    eq_(len(txs), 1)
    eq_(txs[0].parsed_tx, p_tx)
