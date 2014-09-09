from io import DEFAULT_BUFFER_SIZE
from . import CipherBase


class CipherNone(CipherBase):
    BLOCKSIZE = DEFAULT_BUFFER_SIZE

    mode = 'none'

    def __init__(self, key, input=None):
        pass

    def encipher_block(self, block):
        return block

    def decipher_block(self, block):
        return block

    def flush(self):
        return super(CipherNone, self).flush()

    def _pad(self, s):
        return s

    def _unpad(self, s):
        return s
