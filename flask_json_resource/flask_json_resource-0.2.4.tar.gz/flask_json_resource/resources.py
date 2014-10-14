import hashlib
import json
import os

import json_resource

from . import views


class Schema(json_resource.Schema):
    default_views = [views.SchemaView]
    meta = {}

    @property
    def etag(self):
        return hashlib.md5(json.dumps(self)).hexdigest()

    def _from_disk(self):
        for dir in self._schema_dirs:
            try:
                with open(os.path.join(dir, self['id'])) as f:
                    return json.load(f)
            except OSError:
                pass

        raise json_resource.ResourceNotFound(self)

    def load(self):
        self.update(self._from_disk())

    def exists(self):
        self._from_disk()

    def save(self, *args, **kwargs):
        raise NotImplementedError()

    def insert(self, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, *args, **kwargs):
        raise NotImplementedError()
