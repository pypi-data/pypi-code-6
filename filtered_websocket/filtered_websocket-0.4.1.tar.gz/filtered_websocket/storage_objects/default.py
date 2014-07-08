import collections

from .base import BaseStorageObject


class StorageObject(BaseStorageObject):

    storage = collections.defaultdict(set)

    def get(self, item):
        return self.storage.get(item)

    def add(self, key, value):
        self.storage[key].add(value)

    def remove(self, key, value):
        self.storage[key].remove(value)

    def __getitem__(self, item):
        return self.get(item)
