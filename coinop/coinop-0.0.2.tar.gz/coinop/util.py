from hashlib import sha256
from binascii import hexlify, unhexlify

def double_hash (s):
    return sha256(sha256(s).digest()).digest()

