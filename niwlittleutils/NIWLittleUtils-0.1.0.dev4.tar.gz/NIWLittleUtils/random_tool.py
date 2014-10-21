import hashlib
import random
import string
import time

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

def get_random_string(length=36, allowed_chars='complex'):
    """Returns a securely generated random string.

    Generate a securely random string with length or allowed
    characters you want.

    If *allowed_chars* is ignored, it's ``string.ascii_letters + 
    string.digits + string.punctuation`` by default (We use Python
    builtin library `string`_ to set value). You can set it to following
    string values or any *allowed_chars* else.

    .. _`string`: http://docs.python.org/3/library/string.html

    .. tabularcolumns:: |l|L|

    =============== =========================
          Value               Meaning
    =============== =========================
    ``'complex'``     string.ascii_letters + 
                      string.digits + 
                      string.punctuation
    --------------- -------------------------
    ``'middle'``      string.ascii_letters + 
                      string.digits + 
                      '-._~'
    --------------- -------------------------
    ``'simple'``      string.ascii_letters +
                      string.digits
    --------------- -------------------------
    ``'lowercase'``   string.ascii_lowercase
    --------------- -------------------------
    ``'uppercase'``   string.ascii_uppercase
    --------------- -------------------------
    ``'digits'``      string.digits
    =============== =========================

    >>> get_random_string(8) # doctest: +SKIP
    'Qi4Y_fA5'

    >>> get_random_string(5, '0123456789abcdef') # doctest: +SKIP
    '06aef'

    >>> get_random_string(5, 'digits') # doctest: +SKIP
    '05154'

    :param length: Random string length.
    :param allowed_chars: Character allowed to use to generate.
        There has 5 default setting (case-insensitive).
    :type length: int
    :type allowed_chars: str
    :return: A securely generated random string.
    :rtype: str
    """
    case = {
        'complex': string.ascii_letters + string.digits + string.punctuation,
        'middle': string.ascii_letters + string.digits + '-._~',
        'simple': string.ascii_letters + string.digits,
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits
    }

    allowed_chars = case.get(allowed_chars.lower() or 'complex', allowed_chars)

    if not using_sysrandom:
        random.seed(
            hashlib.sha256(
                ("{}{}".format(
                    time.time(),
                    random.getstate(),
                    )).encode('utf-8')
            ).digest())
    return ''.join(random.choice(allowed_chars) for _ in range(length))
