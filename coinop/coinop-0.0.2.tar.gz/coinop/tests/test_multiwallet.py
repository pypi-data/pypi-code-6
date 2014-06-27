import pytest
import yaml

from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret
from bitcoin.core import Hash160

from binascii import hexlify, unhexlify
from coinop.bit.multiwallet import MultiWallet
from coinop.bit.script import Script
from coinop.bit.transaction import Transaction


@pytest.fixture
def generated():
    return MultiWallet.generate(["primary", "backup"])

@pytest.fixture
def wallet_data():
    with open(u"coinop/tests/data/multi_wallet.yaml", u"r") as file:
        data = yaml.load(file)
    return data

@pytest.fixture
def imported_wallet(wallet_data):
    private = wallet_data['private']
    return MultiWallet(private=private)

@pytest.fixture
def transaction_data():
    with open(u"coinop/tests/data/unsigned_payment.yaml", u"r") as file:
        data = yaml.load(file)
    return data

@pytest.fixture
def transaction(transaction_data):
    return Transaction(data=transaction_data)

@pytest.fixture
def limited_wallet(imported_wallet):
    private = dict(primary=imported_wallet.private_seed('primary'))
    public = imported_wallet.public_seeds()
    return MultiWallet(private=private, public=public)


def test_properties(generated):
    assert sorted(generated.trees.keys()) == ["backup", "primary"]
    assert sorted(generated.private_trees.keys()) == ["backup", "primary"]
    assert generated.public_trees.keys() == []

def test_individual_seeds(generated):
    seed = generated.private_seed("backup")
    assert seed.find("tprv") == 0

    seed = generated.public_seed("backup")
    assert seed.find("tpub") == 0

def test_private_seeds(generated):
    for name, seed in generated.private_seeds().iteritems():
        assert seed.find("tprv") == 0

def test_reconstructing_from_seeds(generated):
    reconstructed = MultiWallet(private=generated.private_seeds())
    assert generated.private_seeds() == reconstructed.private_seeds()

def test_node_for_path(imported_wallet, wallet_data):
    for path, values in wallet_data['paths'].iteritems():
        node = imported_wallet.path(path)
        address = node.address()

        assert values["address"] == address
        #multisig_script = node.script()
        #assert values["multisig_script"] == multisig_script.to_string()


def test_compatibility(imported_wallet, wallet_data):
    for path, values in wallet_data['paths'].iteritems():
        node = imported_wallet.path(path)
        multisig_script = node.script()
        assert values["multisig_script"] == multisig_script.to_string()

def test_signing(transaction, limited_wallet):
    inputs = limited_wallet.signatures(transaction)
    assert isinstance(inputs, list)
    assert isinstance(inputs[0], dict)
    assert inputs[0].keys() == ['primary']
    


