# encoding=utf-8
'''Miscellaneous functions.'''
import calendar
import codecs
import contextlib
import datetime
import os.path
import re
import sys
import time
import zipfile


class ASCIIStreamWriter(codecs.StreamWriter):
    '''A Stream Writer that encodes everything to ASCII.

    By default, the replacement character is a Python backslash sequence.
    '''
    DEFAULT_ERROR = 'backslashreplace'

    def __init__(self, stream, errors=DEFAULT_ERROR):
        codecs.StreamWriter.__init__(self, stream, errors)

    def encode(self, instance, errors=DEFAULT_ERROR):
        return instance.encode('ascii', errors)

    def decode(self, instance, errors=DEFAULT_ERROR):
        return instance.encode('ascii', errors)

    def write(self, instance):
        if hasattr(instance, 'encode'):
            instance = instance.encode('ascii', self.errors)

        if hasattr(instance, 'decode'):
            instance = instance.decode('ascii', self.errors)

        self.stream.write(instance)

    def writelines(self, list_instance):
        for item in list_instance:
            self.write(item)


@contextlib.contextmanager
def reset_file_offset(file):
    '''Reset the file offset back to original position.'''
    offset = file.tell()
    yield
    file.seek(offset)


def peek_file(file, length=4096):
    '''Peek the file by calling ``read`` on it.'''
    with reset_file_offset(file):
        return file.read(length)


def datetime_str():
    '''Return the current time in simple ISO8601 notation.'''
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def parse_iso8601_str(string):
    '''Parse a fixed ISO8601 datetime string.

    .. Note:: This function only parses dates in the format
       ``%Y-%m-%dT%H:%M:%SZ``. You must use a library like ``dateutils``
       to properly parse dates and times.

    Returns:
        float: A UNIX timestamp.
    '''
    datetime_obj = datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")
    return int(calendar.timegm(datetime_obj.utctimetuple()))


def python_version():
    '''Return the Python version as a string.'''
    major, minor, patch = sys.version_info[0:3]
    return '{0}.{1}.{2}'.format(major, minor, patch)


def filter_pem(data):
    '''Processes the bytes for PEM certificates.

    Returns:
        ``set`` containing each certificate
    '''
    assert isinstance(data, bytes)
    certs = set()
    new_list = []
    in_pem_block = False

    for line in re.split(br'[\r\n]+', data):
        if line == b'-----BEGIN CERTIFICATE-----':
            assert not in_pem_block
            in_pem_block = True
            new_list.append(line)
        elif line == b'-----END CERTIFICATE-----':
            assert in_pem_block
            in_pem_block = False
            new_list.append(line)

            # Add trailing new line
            new_list.append(b'')

            certs.add(b'\n'.join(new_list))

            new_list = []
        elif in_pem_block:
            new_list.append(line)

    return certs


def truncate_file(path):
    '''Truncate the file.'''
    with open(path, 'wb'):
        pass


def get_package_data(filename, mode='rb'):
    '''Return the contents of a real file or a zip file.'''
    if os.path.exists(filename):
        with open(filename, mode=mode) as in_file:
            return in_file.read()
    else:
        parts = os.path.normpath(filename).split(os.sep)

        for part, index in zip(parts, range(len(parts))):
            if part.endswith('.zip'):
                zip_path = os.sep.join(parts[:index + 1])
                member_path = os.sep.join(parts[index + 1:])

        with zipfile.ZipFile(zip_path) as zip_file:
            return zip_file.read(member_path)


def get_package_filename(filename, package_dir=None):
    '''Return the filename of the data file.'''
    if getattr(sys, 'frozen', False):
        package_dir = os.path.dirname(sys.executable)
    elif not package_dir:
        package_dir = os.path.dirname(__file__)

    return os.path.join(package_dir, filename)
