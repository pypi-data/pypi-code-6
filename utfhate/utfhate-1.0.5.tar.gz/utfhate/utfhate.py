import six

def continuation(integer):
    return byteliteral(integer)[-6:]

def binarycp(*args):
    """
    [internal!] utfhate.binarycp
    ------------------------------------------------
    Helper function which turns a number of integers
    into a list of binary strings. Works for a single
    argument (simple UTF-8 character) or many
    (multi-part with continuation bytes).

    May raise ValueError if input of an unexpected
    length  is encountered, e.g. not 0 < x < 7.
    ------------------------------------------------
    @param  args     list
                     integer
    @return          list
    """
    if not len(args):
        raise ValueError('UTF-8 sequence too short')
        pass
    elif len(args) == 1:
        return [byteliteral(args[0])[-7:]]
    elif len(args) < 7:
        leadbits = abs(len(args) - 7)
        return [byteliteral(args[0])[-leadbits:]] + map(continuation, args[1:])
    else:
        raise ValueError('UTF-8 continuation sequence too long')
        pass
    return

def integercp(*args):
    return int(''.join(args), 2)

def htmlentity(integer):
    return '&#%d;' % integer


def hexliteral(integer):
    return hex(integer)[2:]


def byteliteral(integer):
    return bin(integer)[2:].zfill(8)


def utfentity(*args):
    return htmlentity(integercp(*binarycp(*args)))


def ascii(string):
    return six.text_type(string.encode('ascii'))


def multipart(char, iterable):
    """
    [internal!] utfhate.multipart
    ------------------------------------------------
    Helper function which handles multipart UTF-8
    characters and turns multiple input characters
    from iterable into a single output html entity.
    ------------------------------------------------
    @param  char     character
    @param  iterable iterable
    @return          (html entity, character)
    """
    bytes = [ord(char)]
    while True:
        try:
            char = iterable.next()
            pass
        except StopIteration:
            char = None
            break
            pass

        integer = ord(char)

        if integer in xrange(128, 192):
            bytes.append(integer)
        else:
            break
            pass
        pass
    entity = utfentity(*bytes)

    return (entity, char)


def htmlstring(chars, html_literal=False):
    """
    utfhate.htmlstring
    ------------------------------------------------
    From a unicode, byte-string or something that
    iterates over characters, safely create a valid
    string of html entities.

    Optionally set html_literal=True to receive an
    output with html encoded less than and greater
    than signs for (e.g.) rendering html as text.
    ------------------------------------------------
    @param  chars        string or iterable
    @param  html_literal boolean
    @return              generator
    """
    if not hasattr(chars, '__next__'):
        chars = iter(chars)
        pass

    def generate_htmlstring():
        char = None

        while True:
            char = char or chars.next()
            bytestring = isinstance(char, six.binary_type)
            integer = ord(char)

            if bytestring and integer in xrange(192, 256):
                entity, char = multipart(char, chars)
                yield entity
                continue
                pass
            elif integer > 127 or (html_literal and integer in [60, 62]):
                if bytestring:
                    yield utfentity(integer)
                    pass
                else:
                    yield htmlentity(integer)
                    pass
                pass
            else:
                yield ascii(char)
                pass
            char = None
            pass
        pass
    return generate_htmlstring()
