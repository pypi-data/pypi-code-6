"""
Storage engine of Znap2 library.
"""

import operator
import os
import shutil
import ConfigParser


class SnapshotInfo(object):
    """Snapshot info record."""

    def __init__(self, id, time):
        self.id = id
        self.time = time

    def __str__(self):
        return '<SnapshotInfo(id={id}, time={time})>'.format(**self.__dict__)


class Storage(object):
    """Storage for snapshots."""

    def __init__(self, root_path):
        self.root_path = root_path
        self.dbs = []
        self.db_offsets = {}
        self.initialized = False

    @property
    def storage_path(self):
        """Path to the storage dir."""
        return os.path.join(self.root_path, '.znap2')

    @property
    def config_path(self):
        return os.path.join(self.storage_path, 'config.ini')

    def _get_db_path(self, db):
        """Return the path to specific database file."""
        return os.path.join(self.root_path, db)

    def add(self, db):
        """Add a database to the list of tracked databases."""
        if self.initialized:
            raise ValueError("Can't add a database to an initialized storage.")
        self.dbs.append(db)
        self.db_offsets[db] = os.stat(self._get_db_path(db)).st_size

    def _write_config(self):
        """Write the config to ``.znap2/config.ini``."""
        config = ConfigParser.ConfigParser()
        for db in self.dbs:
            config.add_section(db)
            config.set(db, 'offset', str(self.db_offsets[db]))
        with open(self.config_path, 'wt') as fp:
            config.write(fp)

    def _read_config(self):
        """Read the config from ``.znap2/config.ini``."""
        config = ConfigParser.ConfigParser()
        with open(self.config_path, 'rt') as fp:
            config.readfp(fp)
        for db in config.sections():
            self.dbs.append(db)
            self.db_offsets[db] = config.getint(db, 'offset')

    def init(self):
        """Initialize the storage and write the config to the disk."""
        if self.initialized:
            raise ValueError("Storage already initialized.")
        os.mkdir(self.storage_path)
        self._write_config()
        self.initialized = True

    def load(self):
        """Load the storage from a config file."""
        if self.dbs:
            raise ValueError("Some dbs have been added already.")
        if self.initialized:
            raise ValueError("Storage already initialized.")
        self._read_config()
        self.initialized = True

    def list_ids(self):
        """List available snapshot ids."""
        return [item for item in os.listdir(self.storage_path)
                if item != 'config.ini']

    def describe(self, snapshot_id):
        """Return the description for specific snapshot.

        See :class:`SnapshotInfo` for description of the fields.
        """
        snapshot_path = self._get_snapshot_path(snapshot_id)
        if not os.path.exists(snapshot_path):
            raise ValueError("Invalid snapshot id.")
        return SnapshotInfo(snapshot_id, os.stat(snapshot_path).st_mtime)

    def list(self, order_by='time'):
        """List existing snapshots.

        Returns a list of :class:`SnapshotInfo`.
        """
        return sorted(map(self.describe, self.list_ids()),
                key=operator.attrgetter(order_by))

    def _get_snapshot_path(self, snapshot_id):
        """Return the path of the snapshot."""
        return os.path.join(self.storage_path, snapshot_id)

    def _get_paths_for(self, db, base=None):
        """Return database and index paths for the database."""
        if base is None:
            base = self.root_path
        return (os.path.join(base, db), os.path.join(base, db + '.index'))

    def _save_db(self, snapshot_path, db):
        """Make snapshot part related to specific database."""
        src_db, src_idx = self._get_paths_for(db)
        dst_db, dst_idx = self._get_paths_for(db, base=snapshot_path)
        shutil.copy(src_idx, dst_idx)
        with open(src_db, 'rb') as src_fp, open(dst_db, 'wb') as dst_fp:
            src_fp.seek(self.db_offsets[db])
            shutil.copyfileobj(src_fp, dst_fp)

    def save(self, snapshot_id):
        """Save a new snapshot under specified id."""
        snapshot_path = self._get_snapshot_path(snapshot_id)
        if os.path.exists(snapshot_path):
            raise ValueError("Duplicate snapshot id.")
        os.mkdir(snapshot_path)
        for db in self.dbs:
            self._save_db(snapshot_path, db)

    def _restore_db(self, snapshot_path, db):
        """Restore snapshot part related to specific database."""
        src_db, src_idx = self._get_paths_for(db, base=snapshot_path)
        dst_db, dst_idx = self._get_paths_for(db)
        shutil.copy(src_idx, dst_idx)
        with open(src_db, 'rb') as src_fp, open(dst_db, 'a+b') as dst_fp:
            dst_fp.truncate(self.db_offsets[db])
            dst_fp.seek(self.db_offsets[db])
            shutil.copyfileobj(src_fp, dst_fp)

    def restore(self, snapshot_id):
        """Restore snapshot by id."""
        snapshot_path = self._get_snapshot_path(snapshot_id)
        if not os.path.exists(snapshot_path):
            raise ValueError("Invalid snapshot id.")
        for db in self.dbs:
            self._restore_db(snapshot_path, db)

    def delete(self, snapshot_id):
        """Delete snapshot by id."""
        snapshot_path = self._get_snapshot_path(snapshot_id)
        if not os.path.exists(snapshot_path):
            raise ValueError("Invalid snapshot id.")
        shutil.rmtree(snapshot_path)
