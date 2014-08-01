import lib

def htmlstring(chars, lazy=False):
    if not hasattr(chars, '__next__'):
        chars = iter(chars)
        pass

    def generator():
        char = None
        while True:
            char = char or chars.next()
            decimal = ord(char)

            if decimal in xrange(192, 256):
                entity, char = lib.multipart(char, chars)
                yield entity
                continue
            elif decimal in [60, 62]:
                yield lib.utfentity(decimal)
            else:
                yield char
            char = None
    return generator() if lazy else ''.join(list(generator()))
