import sqlite3

MAX_KEY_SIZE = 256

_CREATE_TABLES = """\
CREATE TABLE IF NOT EXISTS queue
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key STRING({max_key_size}) UNIQUE,
    value BLOB,
    modified_at INT NOT NULL
);
""".format(max_key_size=MAX_KEY_SIZE)

_TABLE_SIZE = "SELECT COUNT(id) FROM Queue;"

_DELETE_OLDEST = """\
DELETE
    FROM queue
    WHERE id = (
        SELECT id FROM queue
        ORDER BY modified_at ASC
        LIMIT 1
    );
"""

_DELETE_KEY = "DELETE FROM queue WHERE key = ?;"

_WRITE = """
INSERT OR REPLACE
    INTO queue (key, value, modified_at)
    VALUES( ?, ?, time('now'));
"""


class SQLiteCache(object):
    """
    A simple K/V cache with a max capacity.

    When the cache reaches its capacity, older entries are overwritten.

    Parameters
    ----------
    uri: str
        Sqlite connection string (e.g. 'foo.db', or ':memory:')
    capacity: int
        Maximum number of entries.
    """
    def __init__(self, uri, capacity=10):
        self._uri = uri
        self._capacity = capacity
        self._cx = sqlite3.Connection(self._uri)

        self._cx.execute("pragma synchronous = off;")
        self._cx.execute(_CREATE_TABLES)

        self._closed = False

    def close(self):
        """
        Close the cache.

        SQLite connection is closed, you cannot use any get/set/delete anymore.
        """
        self._closed = True
        self._cx.close()

    def __enter__(self):
        return self

    def __exit__(self, *a, **kw):
        self.close()

    @property
    def capacity(self):
        return self._capacity

    @property
    def closed(self):
        return self._closed

    def size(self):
        c = self._cx.cursor()
        try:
            res = c.execute(_TABLE_SIZE)
            return res.fetchone()[0]
        finally:
            c.close()

    def get(self, key):
        """
        Retrieve the entry for the given key
        """
        c = self._cx.cursor()
        try:
            res = c.execute("SELECT value FROM queue WHERE key = ?;", (key,))
            row = res.fetchone()
            if row:
                return row[0]
            else:
                return None
        finally:
            c.close()

    def set(self, key, value):
        """
        Write the given value for the given key
        """
        c = self._cx.cursor()
        try:
            res = c.execute(_TABLE_SIZE)
            size = res.fetchone()[0]
            if size >= self.capacity:
                c.execute(_DELETE_OLDEST)
            c.execute(_WRITE, (key, value))
            self._cx.commit()
        finally:
            c.close()

    def delete(self, key):
        """
        Delete the given key, value pair

        Does not raise an exception if the key does not exist.
        """
        c = self._cx.cursor()
        try:
            res = c.execute("SELECT value FROM queue WHERE key = ?;", (key,))
            row = res.fetchone()
            if row:
                c.execute(_DELETE_KEY, (key,))
            self._cx.commit()
        finally:
            c.close()
