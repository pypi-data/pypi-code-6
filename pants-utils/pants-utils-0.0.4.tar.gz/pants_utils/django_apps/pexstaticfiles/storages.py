import pkg_resources
import sys

from django.core.files.storage import Storage
from django.core.files.base import File

class EggStorage(Storage):
    '''
    Assumes that absolute path is:
    <module>/<resource_path>

    Read-only Storage. Raise NotImplemented if attempt to write
    '''

    def __init__(self, module):
        self.module = module

    def _open(self, name, mode='rb'):
        return File(pkg_resources.resource_stream(self.module, name))

    def _save(self, name, content):
        raise NotImplementedError("This backend is read-only")

    def exists(self, name):
        return pkg_resources.resource_exists(self.module, name)

    def listdir(self, name):
        directories, files = [], []
        for entry in pkg_resources.resource_listdir(self.module, name):
            if pkg_resources.resource_isdir(self.module, entry):
                directories.append(entry)
            else:
                files.append(entry)
        return directories, files

    def size(self, name):
        return sys.getsizeof(self._open(name))
