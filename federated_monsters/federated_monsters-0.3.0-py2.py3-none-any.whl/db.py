# -*- coding: utf-8 -*-

"""This module contains the BerkeleyDB class."""
try:
    from global_vars import *
except ImportError:
    from federated_monsters.global_vars import *


class DB(object):

    """A template class for other DB classes.

    It is designed so that others can easily create classes for different
    databases if they so desire.

    Attributes:
        db (bsddb3.DB): The db on which the class can operate.
    """

    def __init__(self):
        """Init DB class."""
        self.db = object()
        pass

    def open_db(self):
        """Open the DB for reading and writing.

        Returns:
            bool: True if successful, False if error encountered.
        """
        return True

    def add_entry(self, hash_digest, value):
        """Add an entry to the database and sync it.

        Args:
            hash_digest (str): The digest of the SHA512 hash of the entry.
            value (str): The JSON serialization of the monster.

        Returns:
            bool: True if successful, False if error encountered.
        """
        return True

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
        return ""

    def remove_entry(self, hash_digest):
        """Remove an entry to the database and sync it.

        Args:
            hash_digest (str): The digest of the SHA512 hash of the entry.

        Returns:
            bool: True if successful, False if error encountered.
        """
        return True

    def all_db(self):
        """Retrieve all entries in the database.

        Returns:
            dict: A dict mapping keys to the retrieved values.
        """
        return {}

    def close(self):
        """Close the database."""
        pass


class DBException(Exception):

    """A generic error to represent all errors associated with DB operations.

    Attributes:
        value (str): The string value of the exception.
    """

    def __init__(self, value):
        """Init the DBError with value."""
        self.value = value

    def __str__(self):
        """Return the string representation of the exception."""
        return repr(self.value)
