from StringIO import StringIO
import hashlib
import json

import logging
logger = logging.getLogger(__name__)


class Manager(object):
    DATA_FILE = "backup_data.json"

    def __init__(self, remote):
        self.remote = remote

    def build_filename(self, unique_name):
        m = hashlib.md5()
        m.update(unique_name)
        return "%s.gz" % m.hexdigest()

# -----

    def pull_data(self):
        data = self.remote.pull(self.DATA_FILE).read()
        try:
            data = json.loads(data)
        except ValueError:
            data = {}
        return data

    def push_data(self):
        stream = StringIO(json.dumps(self.data))
        self.remote.push(stream, self.DATA_FILE)

    @property
    def data(self):
        # Lazy data pulling
        if not hasattr(self, '_cached_data'):
            self._cached_data = self.pull_data()
        return self._cached_data

# -----

    def push_backup(self, creator):
        checksum = creator.checksum()

        filename = self.build_filename(creator.unique_name)
        if creator.TYPE not in self.data:
            self.data[creator.TYPE] = {}

        if filename in self.data[creator.TYPE]:
            creator_data = self.data[creator.TYPE][filename]
            if checksum == creator_data['checksum']:
                logger.info('Backup already exists with the same version: %s (%s)' % (filename, creator.TYPE))
                return

        stream = creator.create()
        self.remote.push(stream, filename)

        self.data[creator.TYPE][filename] = {
            'data': creator.data,
            'checksum': checksum
        }

        self.push_data()

    def restore_backup(self, restorer):
        pass
