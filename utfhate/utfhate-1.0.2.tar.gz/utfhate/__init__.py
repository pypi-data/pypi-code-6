import six
import lib

def htmlstring(chars, lazy=False, literal=False,):
    if not hasattr(chars, '__next__'):
        chars = iter(chars)
        pass

    def generator():
        char = None

        while True:
            char = char or chars.next()
            bytestring = isinstance(char, six.binary_type)
            decimal = ord(char)

            if bytestring and decimal in xrange(192, 256):
                entity, char = lib.multipart(char, chars)
                yield entity
                continue
                pass
            elif decimal > 127 or (literal and decimal in [60, 62]):
                if bytestring:
                    yield lib.utfentity(decimal)
                    pass
                else:
                    yield lib.htmlentity(decimal)
                    pass
                pass
            else:
                yield lib.ascii(char)
                pass
            char = None
            pass
        pass
    return generator() if lazy else ''.join(list(generator()))

