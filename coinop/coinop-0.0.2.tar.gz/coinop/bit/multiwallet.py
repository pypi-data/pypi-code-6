from binascii import hexlify, unhexlify

from nacl.utils import random
from pycoin.key import bip32

from .script import Script
from .keys import PrivateKey, PublicKey

import bitcoin.base58 as base58

class MultiWallet(object):

    @classmethod
    def generate(cls, names, network="testnet"):
        seeds = {}
        def create_node(name):
            secret = random(32)
            # FIXME: set blockchain/network correctly
            tree = bip32.Wallet.from_master_secret(secret, netcode='XTN')
            return tree

        for name in names:
            seeds[name] = create_node(name).wallet_key(as_private=True)

        return cls(private=seeds)


    def __init__(self, private={}, public={}):
        self.trees = {}
        self.private_trees = {}
        self.public_trees = {}

        for name, seed in private.iteritems():
            tree = bip32.Wallet.from_wallet_key(seed)
            self.private_trees[name] = self.trees[name] = tree

        for name, seed in public.iteritems():
            tree = bip32.Wallet.from_wallet_key(seed)
            self.public_trees[name] = self.trees[name] = tree

    def to_dict(self):
        return dict(private=self.private_seeds(), public=self.public_seeds())

    def private_seed(self, name):
        try:
            return self.private_trees[name].wallet_key(as_private=True)
        except KeyError:
            raise Exception("No private tree for '{0}'".format(name))


    def public_seed(self, name):
        tree = self.public_trees.get(name, None)
        if not tree:
            tree = self.private_trees.get(name, None)
        if not tree:
            raise Exception("No public tree for '{0}'".format(name))
        return tree.wallet_key()


    def private_seeds(self):
        out = {}
        for name, tree in self.private_trees.iteritems():
            out[name] = self.private_seed(name)
        return out
        

    def public_seeds(self):
        out = {}
        for name, tree in self.public_trees.iteritems():
            out[name] = self.public_seed(name)
        return out
        

    def path(self, path):
        _path = path[2:]
        options = { 'private': {}, 'public': {} }

        for name, tree in self.private_trees.iteritems():
            options['private'][name] = tree.subkey_for_path(_path)
        for name, tree in self.public_trees.iteritems():
            options['public'][name] = tree.subkey_for_path(_path)

        return MultiNode(path, **options)

    def is_valid_output(self, output):
        path = output.metadata['wallet_path']
        node = self.path(path)
        # TODO: use python equiv of ruby to_s
        # apparently the global str() ?
        ours = node.p2sh_script().to_string()
        theirs = output.script.to_string()
        return ours == theirs

    def signatures(self, transaction):
        return map(self.sign_input, transaction.inputs)

    def sign_input(self, input):
        path = input.output.metadata['wallet_path']
        node = self.path(path)
        sig_hash = input.sig_hash(node.script())
        return node.signatures(sig_hash)


class MultiNode:

    def __init__(self, path, private={}, public={}):
        self.path = path
        self.private = private
        self.public = public

        self.private_keys = {}
        self.public_keys = {}

        for name, node in private.iteritems():
            priv = PrivateKey.from_secret(node.secret_exponent_bytes)
            self.private_keys[name] = priv

            pub = priv.public_key()
            self.public_keys[name] = pub

        for name, node in public.iteritems():
            pub = PublicKey.from_pair(node.public_pair)
            self.public_keys[name] = pub
            pass

    def script(self, m=2):
        names = sorted(self.public_keys.keys())
        keys = [self.public_keys[name].compressed() for name in names]

        return Script(public_keys=keys, needed=m)

    def address(self):
        return self.script().p2sh_address()


    def p2sh_script(self):
        return Script(p2sh_address=self.address())

    def signatures(self, value):
        names = sorted(self.private_keys.keys())
        #return dict((name, self.sign(name, value)) for name in names)
        s = ((name, base58.encode(self.sign(name, value))) for name in names)
        return dict(s)

    def sign(self, name, value):
        try:
            key = self.private_keys[name]
            # \x01 means the hash type is SIGHASH_ALL
            # https://en.bitcoin.it/wiki/OP_CHECKSIG#Hashtype_SIGHASH_ALL_.28default.29
            return key.sign(value) + b'\x01'
        except KeyError:
            raise Exception("No such key: '{0}'".format(name))


    def script_sig(self, signatures):
        self.script.p2sh_sig(signatures=signatures)


