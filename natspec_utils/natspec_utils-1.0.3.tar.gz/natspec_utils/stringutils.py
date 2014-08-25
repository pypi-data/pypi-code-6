import sys

def stringToUnicode(x):
    """
    This function return a unicode string for all python versions
    """
    if sys.version < '3':
        import codecs
        return codecs.unicode_escape_decode(x)[0]
    return x