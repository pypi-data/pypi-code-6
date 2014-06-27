import pytest
import yaml
from binascii import hexlify, unhexlify

from coinop.bit.transaction import Transaction
from coinop.bit.script import Script, from_string

from bitcoin.core.serialize import Hash
from bitcoin.core import b2lx
import bitcoin.base58 as base58


@pytest.fixture
def transaction_data():
    with open(u"coinop/tests/data/unsigned_payment.yaml", u"r") as file:
        data = yaml.load(file)
    return data



def test_from_data(transaction_data):
    input = transaction_data['inputs'][0]
    data_sig_hash = input['sig_hash']

    tx = Transaction(data=transaction_data)

    redeem_script = Script(string=transaction_data['redeem_script'])
    sig_hash = tx.inputs[0].sig_hash(redeem_script)

    assert hexlify(sig_hash) == data_sig_hash





