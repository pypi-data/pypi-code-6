import pytest
import yaml

from hashlib import sha256
from binascii import hexlify, unhexlify
#from nacl.utils import random

from pycoin.key import Key, bip32
from pycoin.encoding import public_pair_to_sec
from pycoin.networks import wif_prefix_for_netcode



from coinop.bit.keys import PrivateKey, PublicKey


#@pytest.fixture
#def wallet():
    #secret = random(32)
    #return bip32.Wallet.from_master_secret(secret, netcode='XTN')


def test_key_stuff():
    with open(u"coinop/tests/data/multi_wallet.yaml", u"r") as file:
        data = yaml.load(file)

    seed = data['private']['primary']
    path = data['paths']['m/0/0/0']

    digest = unhexlify(path['digest'])
    # the last byte is added for some bitcoin reason. TODO: document
    rb_sig = unhexlify(path['primary_signature'])[:-1]

    wallet = bip32.Wallet.from_wallet_key(seed)
    node = wallet.subkey_for_path('0/0/0')

    assert path['primary_seed'] == node.wallet_key(as_private=True)
    assert path['primary_address'] == node.bitcoin_address()
    assert path['primary_hex'] ==  hexlify(node.secret_exponent_bytes)


    priv = PrivateKey.from_secret(node.secret_exponent_bytes)
    pub = priv.public_key()

    py_sig = priv.sign(digest)
    pub.verify(digest, py_sig)

    pub.verify(digest, rb_sig)

    pub2 = PublicKey.from_string(pub.to_string())
    pub2.verify(digest, rb_sig)

    sec = public_pair_to_sec(node.public_pair, compressed=False)[1:]
    pub_from_node = PublicKey.from_string(sec)
    pub_from_node.verify(digest, rb_sig)

    x, y = node.public_pair
    pub_from_pair = PublicKey.from_pair(node.public_pair)

    pub_from_pair.verify(digest, rb_sig)







    

