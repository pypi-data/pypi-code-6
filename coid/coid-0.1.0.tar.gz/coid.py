"""
Simple codecs for uuiids. Can be useful when you represent ids differently
between domains. Use it e.g. like:

.. code:: python

    import uuid
    import coid
    
    id = uuid.uuid4()
    
    id_codec = coid.Id(prefix='BLA-', encoding='base58')
    assert id == id_codec.decode(id_codec.encode(id))
    
and if you have a pile of codecs you could decode conveniently e.g. like:

.. code:: python

    import uuid
    import coid
    
    id = uuid.uuid4()
    
    ids_codec = coid.Ids([
        coid.Id(prefix='CD1-', encoding='base58')
        coid.Id(prefix='CD1-', encoding='base58')
        coid.Id(prefix='CD1-', encoding='base58')
    ])
    
    id = uuid.uuid4()
    encoded_ id = ids_codec.ids[0].encode(id)
    
    assert id == ids_codec.decode(encoded_ id)

"""
from __future__ import unicode_literals, absolute_import

import codecs
import uuid


__version__ = '0.1.0'


class Id(object, codecs.Codec):

    def __init__(self, encoding='hex', prefix=None):
        if encoding == 'hex':
            self._encode, self._decode = lambda x: '{:032x}'.format(x), lambda x: int(x, 16)
        elif encoding == 'base58':
            self._encode, self._decode = lambda x: base58_encode(x).zfill(22), base58_decode
        elif encoding == 'base62':
            self._encode, self._decode = lambda x: base62_encode(x), base62_decode
        else:
            raise ValueError('Invalid encoding {}'.format(encoding))
        self.encoding = encoding
        self.prefix = prefix

    def encode(self, input, errors='strict'):
        if not isinstance(input, uuid.UUID):
            raise TypeError(
                'Expected instance of {} not {}'.format(uuid.UUID, type(input))
            )
        encoded = self._encode(input.int)
        if self.prefix:
            value = '{}{}'.format(self.prefix, encoded)
        else:
            value = encoded
        return value

    def decode(self, input, errors='strict'):
        if not isinstance(input, basestring):
            raise TypeError(
                'Expected instance of {} not {}'
                .format(basestring, type(input))
            )
        encoded = input
        if self.prefix:
            if not input.startswith(self.prefix):
                raise ValueError('Does not start with "{}"'.format(self.prefix))
            encoded = encoded[len(self.prefix):]
        decoded = self._decode(encoded)
        return uuid.UUID(int=decoded)


class Ids(object, codecs.Codec):

    def __init__(self, ids):
        self.ids = ids

    def encode(self, input, errors='strict'):
        raise NotImplementedError('Ambiguous')

    def decode(self, input, errors='strict'):
        for id in self.ids:
            try:
                return id.decode(input)
            except ValueError:
                pass
        raise ValueError('Does "{}" not match any encoding'.format(input))


def is_encoded(input, codec):
    try:
        codec.decode(input)
        return True
    except (ValueError, TypeError):
        return False


# NOTE: based on https://gist.github.com/ianoxley/865912

def base_encode(num, alphabet, base):
    encode = ''

    if (num < 0):
        return ''

    while (num >= base):
        mod = num % base
        encode = alphabet[mod] + encode
        num = num / base

    if (num):
        encode = alphabet[num] + encode

    return encode


def base_decode(s, alphabet, base):
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * alphabet.index(char)
        multi = multi * base

    return decoded


base58_alphabet = '0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


def base58_encode(num):
    return base_encode(num, base58_alphabet, 58)


def base58_decode(s):
    return base_decode(s, base58_alphabet, 58)


base62_alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def base62_encode(num):
    return base_encode(num, base62_alphabet, 62)


def base62_decode(s):
    return base_decode(s, base62_alphabet, 62)
