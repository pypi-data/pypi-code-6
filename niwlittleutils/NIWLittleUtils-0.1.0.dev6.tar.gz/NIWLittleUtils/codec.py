import base64
import zlib

def b64encode(b):
    """Base64 encodes a byte string.

    Base64 encodes a byte string. The resulting bytestring
    is safe for putting into URLs. The input ``b`` should be
    a ``bytes`` or ``bytearray`` object in Python3.3 or
    any `bytes-like object`_ after Python3.4. This function
    will raise ``TypeError`` if ``b`` is not
    `bytes-like object`_ (For example, ``str``).

    .. _`bytes-like object`: https://docs.python.org/3/glossary.html#term-bytes-like-object

    :rtype: bytes
    """
    return base64.urlsafe_b64encode(b).strip(b'=')

def b64decode(b):
    """Decode a Base64 encoded byte string.

    Decode a Base64 encoded byte string using a URL-safe
    alphabet, which substitutes ``-`` instead of ``+``
    and ``_`` instead of ``/`` in the standard Base64
    alphabet. The input ``b`` may also be a ASCII-only
    Unicode strings.

    :rtype: bytes
    """
    if isinstance(b, str):
        b = b.encode('ascii')
    return base64.urlsafe_b64decode(b + b'=' * (-len(b) % 4))

def urlsafe_encode(s):
    """Encode a string or byte string to url-safe string.

    Encode a string or byte string to url-safe string.
    The input can be a object of ``str``, ``bytes`` or
    ``bytearray``.

    This function will make sure that return string
    contains characters that *RFC 3986 section 2.3*
    specified only, but it won't check the length.
    User should remember that browsers have limit for
    length of URLs. (For example, IE8's maximum URL
    length is 2083 chars)

    :rtype: str
    """
    is_compressed = False

    if isinstance(s, str):
        is_str = True
        b = s.encode(errors='surrogateescape')
    else:
        is_str = False
        b = s

    compressed = zlib.compress(b, 9)
    if len(compressed) < (len(b) - 1):
        b = compressed
        is_compressed = True
    b64ed = b64encode(b)
    if is_str:
        b64ed = b'~' + b64ed
    if is_compressed:
        b64ed = b'.' + b64ed
    return b64ed.decode()

def urlsafe_decode(s):
    """Decode a string that encode by :func:`~NIWLittleUtils.codec.urlsafe_encode`.

    Decode a string that encoded by
    :func:`~NIWLittleUtils.codec.urlsafe_encode`.
    If the input ``s`` which returned by
    :func:`~NIWLittleUtils.codec.urlsafe_encode`
    is encode from ``bytes`` or ``bytearray``
    object, it will return ``bytes`` object.
    If ``s`` is encode from ``str`` object, it
    will return ``str`` object.

    :rtype: str or bytes
    """
    s = s.encode()

    is_compressed = False
    is_str = False
    if s.startswith(b'.'):
        s = s[1:]
        is_compressed = True
    if s.startswith(b'~'):
        s = s[1:]
        is_str = True

    try:
        b = b64decode(s)
    except Exception as e:
        raise ValueError('Could not base64 decode '
                         'because of an exception: '
                         '{}'.format(e))
    if is_compressed:
        try:
            b = zlib.decompress(b)
        except Exception as e:
            raise ValueError('Could not zlib '
                             'decompress because '
                             'of an exception: '
                             '{}'.format(e))

    return b.decode(errors='surrogateescape') if is_str else b
