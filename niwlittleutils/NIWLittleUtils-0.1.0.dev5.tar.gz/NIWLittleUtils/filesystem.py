import os
import sys
from unicodedata import normalize

_windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1',
'LPT2', 'LPT3', 'PRN', 'NUL')

def secure_filename(filename, codec='utf8'):
    r"""Pass it a filename and it will return a secure version of it.

    This finction is a modified version of |werkzeug-secure_filename|_.

    .. |werkzeug-secure_filename| replace:: ``werkzeug.utils.secure_filename``
    .. _werkzeug-secure_filename: http://werkzeug.pocoo.org/docs/0.9/utils/#werkzeug.utils.secure_filename

    The filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.

    You can use parameter ``codec`` to specify the codec which is used
    to encode the filename. The ``codec`` could only be *utf8* or *ascii*.
    If you need high portability, you should let ``codec`` to be ``'ascii'``.
    It will be ``'utf8'`` by default.

    On windows systems the function also makes sure that the file is not
    named after one of the special device files.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename('i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_ümläuts.txt'
    >>> secure_filename('i contain cool \xfcml\xe4uts.txt', 'ascii')
    'i_contain_cool_umlauts.txt'

    The function might return an empty filename. It's your responsibility
    to ensure that the filename is unique and that you generate random
    filename if the function returned an empty one.

    :param filename: the filename to secure
    """
    if codec.lower() not in ('utf8', 'utf-8', 'ascii'):
        raise ValueError('Argument ``codec`` should be *utf8* or *ascii*.')

    if isinstance(filename, str):
        filename, ext = os.path.splitext(filename)
        filename = normalize('NFKD', filename).encode(codec, 'ignore').decode(codec)
    else:
        raise TypeError('Filename should be a instance of str.')

    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    filename = '_'.join(filename.split()) + ext
    filename = filename.strip('._')

    if os.name == 'nt' and filename and filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename

    return filename
