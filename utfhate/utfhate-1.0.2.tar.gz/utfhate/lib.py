import six

def continuation(decimal):
    return byteliteral(decimal)[-6:]

def binarycp(*args):
    if not len(args):
        raise ValueError('UTF-8 continuation sequence too short')
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

def decimalcp(*args):
    return int(''.join(args), 2)

def htmlentity(decimal):
    return '&#%d;' % decimal

def hexliteral(decimal):
    return hex(decimal)[2:]

def byteliteral(decimal):
    return bin(decimal)[2:].zfill(8)

def utfentity(*args):
    return htmlentity(decimalcp(*binarycp(*args)))

def ascii(string):
    return six.text_type(string.encode('ascii'))

def multipart(char, iterable):
    bytes = [ord(char)]
    while True:
        try:
            char = iterable.next()
            pass
        except StopIteration:
            char = None
            break
            pass

        decimal = ord(char)

        if decimal in xrange(128, 192):
            bytes.append(decimal)
        else:
            break
            pass
        pass
    entity = utfentity(*bytes)

    return (entity, char)
