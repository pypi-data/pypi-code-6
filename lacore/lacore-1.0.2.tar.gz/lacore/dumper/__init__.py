from lacore.source.stream import StreamSource
from lacore.auth import MyHashObj
from lacore.decorators import coroutine
from lacore.adf.elements import Certificate, Archive, Meta, Cipher
from lacore.exceptions import InvalidArchiveError
from lacore.cipher import get_cipher
from lacore.crypt import CryptIO
from abc import ABCMeta, abstractmethod
from shutil import copyfileobj


class Dumper(object):
    __metaclass__ = ABCMeta

    def __init__(self, docs={}, title='', description=None, fmt='zip',
                 hashf='sha512', chunk=100, **kwargs):
        super(Dumper, self).__init__(**kwargs)
        self.hashobj = MyHashObj(hashf)
        self.chunk = chunk
        self.docs = docs
        if 'archive' not in self.docs:
            self.docs['archive'] = Archive(
                title, Meta(fmt, Cipher('aes-256-ctr', 1)),
                description=description)
        if 'cert' not in self.docs:
            self.docs['cert'] = Certificate()

    def update(self, result):
        self.docs.update(result)

    @abstractmethod
    def write(self, data):
        """ write a piece of data to the storage """

    @coroutine
    def uploader(self):
        while True:
            data = yield
            self.write(data)

    @coroutine
    def end(self):
        self.docs['archive'].meta.size = yield
        self.update({'auth': self.hashobj.auth()})

    @coroutine
    def verify(self):
        yield
        if not self.hashobj.verify(self.docs['auth']):
            raise InvalidArchiveError("archive verification failed")
        self.update({})

    def dump(self, items, cb=None):
        if not hasattr(self, 'archive'):
            raise NotImplementedError(
                "you need to inherit from an archiver class")
        with self:
            with StreamSource(self.end(), self.uploader(), self.chunk) as dest:
                cipher = get_cipher(self.docs['archive'], self.docs['cert'])
                with CryptIO(dest, cipher, hashobj=self.hashobj) as fdst:
                    for result in self.archive(items, fdst, cb):
                        yield result

    def dedump(self, infile, chunk=1024):
        cipher = get_cipher(self.docs['archive'], self.docs['cert'])
        with self:
            with StreamSource(self.verify(),
                              self.uploader(), self.chunk) as dest:
                with CryptIO(infile, cipher,
                             hashobj=self.hashobj, mode='rb') as cf:
                    copyfileobj(cf, dest, chunk)

    def __enter__(self):
        return self

    def __exit__(self, eType, eValue, eTrace):
        return
