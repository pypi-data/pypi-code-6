# -*- coding: utf-8 -*-

"""This module contains the BerkeleyDB class."""
import bsddb3
try:
    from db import DB, DBException
except ImportError:
    from federated_monsters.db import DB, DBException
try:
    from global_vars import *
except ImportError:
    from federated_monsters.global_vars import *


class BerkeleyDB(DB):

    """A wrapper class around various Berkeley database functions.

    It is designed so that others can write equivalents for different databases
    if they so desire.

    Attributes:
        db_fn (str, optional): The file name from which the database should be
            loaded. Defaults to "monsters".
        db (bsddb3.DB): The db on which the class can operate.
    """

    def __init__(self, db_fn="monsters_db"):
        """Init the BerkeleyDB class.

        Args:
            db_fn (str, optional): The file name from which the database should
                be loaded. Defaults to "monsters_db".
        """
        super(DB, self).__init__()
        self.db_fn = db_fn
        self.db = bsddb3.db.DB()

    def open_db(self):
        """Open the DB for reading and writing.

        Returns:
            bool: True if successful, False if error encountered.
        """
        try:
            self.db.open(self.db_fn, None, bsddb3.db.DB_HASH,
                         bsddb3.db.DB_CREATE)
            return True
        except bsddb3.db.DBError:
            return False

    def add_entry(self, hash_digest, value):
        """Add an entry to the database and sync it.

        Args:
            hash_digest (str): The digest of the SHA512 hash of the entry.
            value (str): The JSON serialization of the monster.

        Returns:
            bool: True if successful, False if error encountered.
        """
        try:
            self.db.put(hash_digest.encode(ENC_), value)
            self.db.sync()
            return True
        except bsddb3.db.DBError:
            return False

    def get_entry(self, hash_digest):
        """Get an entry from the database.

        Args:
            hash_digest (str): The digest of the SHA512 hash of the entry.

        Returns:
            str or None: The value of the key in the database, or None if it
                does not exist.

        Raises:
            :class:`federated_monsters.db.DBException`: If an error occurs.
        """
        try:
            return self.db.get(hash_digest.encode(ENC_))
        except bsddb3.db.DBError as e:
            raise DBException(e.__str__())

    def remove_entry(self, hash_digest):
        """Remove an entry to the database and sync it.

        Args:
            hash_digest (str): The digest of the SHA512 hash of the entry.

        Returns:
            bool: True if successful, False if error encountered.
        """
        try:
            self.db.delete(hash_digest.encode(ENC_))
            self.db.sync()
            return True
        except bsddb3.db.DBError:
            return False

    def all_db(self):
        """Retrieve all entries in the database.

        Returns:
            dict: A dict mapping keys to the retrieved values.
        """
        arr = {}
        """while rec:
            arr.append(rec)
            rec = cursor.next()"""
        for i in self.db.keys():
            arr[i] = self.db.get(i)
        return arr

    def close(self):
        """Close the database."""
        self.db.close()
