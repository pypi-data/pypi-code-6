from tempfile import NamedTemporaryFile
from lacore.crypt import CryptIO
from lacore.cipher import get_cipher
from shutil import copyfileobj
from zipfile import ZipFile
from abc import ABCMeta, abstractmethod


def restore_archive(archive, path, cert, folder, tmpdir, cb=None):
    cipher = get_cipher(archive, cert)
    with open(path, 'rb') as infile:
        with NamedTemporaryFile() as dst:
            with CryptIO(infile, cipher) as cf:
                copyfileobj(cf, dst)
            dst.flush()
            dst.seek(0)
            with ZipFile(dst) as zf:
                map(cb,
                    map(lambda zi: zf.extract(zi, folder), zf.infolist()))


class Archiver(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def args(self, items, cb=None):
        """ process each item before archiving, calling
            callback if supplied
        """

    @abstractmethod
    def archive(self, items, dest, cb=None):
        """ write every item to test and yield the item """
