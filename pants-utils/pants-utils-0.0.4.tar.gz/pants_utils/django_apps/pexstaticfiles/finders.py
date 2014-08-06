from django.contrib.staticfiles.finders import BaseStorageFinder
from django.contrib.staticfiles import utils
from django.utils.functional import LazyObject
from django.core.files.storage import Storage
from django.conf import settings

from pants_utils.django_apps.pexstaticfiles.storages import EggStorage

class EggFinder(BaseStorageFinder):
    '''
    Finds static assets using EggStorage where EGG_STATIC_DIR is
    the base module from which to access resources using pkg_resources
    '''
    storage = EggStorage

    def __init__(self, storage=None, *args, **kwargs):
        self.module = settings.EGG_STATIC_DIR

        if not isinstance(self.storage, (Storage, LazyObject)):
            self.storage = self.storage(self.module)

        super(EggFinder, self).__init__(self.storage, *args, **kwargs)

    def find(self, path, all=False):
        return path if self.storage.exists(path) else None

    def list(self, ignore_patterns):
        for path in utils.get_files(self.storage, ignore_patterns):
            yield path, self.storage
