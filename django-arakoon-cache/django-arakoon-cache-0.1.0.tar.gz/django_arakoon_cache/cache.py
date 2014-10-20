import time

try:
    import cPickle as pickle
except ImportError:
    import pickle

from arakoon import Arakoon

from django.core.cache.backends.base import BaseCache

KEY_SEP = '::ara::'


def get_arakoon_client(config, cluster='django'):
    arakoon_config = Arakoon.ArakoonClientConfig(cluster, config)
    client = Arakoon.ArakoonClient(arakoon_config)
    return client


class ArakoonCache(BaseCache):

    def __init__(self, server, params):
        super(ArakoonCache, self).__init__(params)

        self._client = None

        self._options = params.get('OPTIONS', {})

        # Important: Cluster ID
        self._cluster = self._options.get('cluster', None)

        # Auto Delete expired Keys
        self._auto_delete_expired = self._options.get('AUTO_DELETE_EXP', True)

        self._config = server

    @property
    def client(self):
        if not self._client:
            self._client = get_arakoon_client(self._config, self._cluster)

        return self._client

    def pickle(self, value):
        """
        Pickle value.
        """
        return pickle.dumps(value)

    def unpickle(self, value):
        """
        Unpickle value.
        """
        return pickle.loads(value)

    def _is_expired(self, ara_key):
        _, timeout = self._get_arakoon_key_details(ara_key)
        now = time.time()

        return timeout < now

    def _get_timeout(self, timeout):
        timeout = timeout or self.default_timeout
        timeout += int(time.time())
        return timeout

    def _make_arakoon_key(self, key, timeout=0, version=None):
        """
        Make arakoon key with timeout included.

        Example:
            key: 'arakey', timeout:10
            result: 'arakey::ara::10'
        """
        default_key = self.make_key(key, version=version)
        timeout = self._get_timeout(timeout)
        return KEY_SEP.join([default_key, str(timeout)])

    def _get_arakoon_key(self, key, version=None):
        key_prefix = self.make_key(key, version=version)

        # Adding KEY_SEP to get exact match!
        keys = self.client.prefix(key_prefix + KEY_SEP, maxElements=1)
        return keys[0] if len(keys) else None

    def _get_arakoon_key_details(self, arakoon_key):
        """
        Return tuple of key and timeout!
        """
        details = arakoon_key.split(KEY_SEP)
        prefix = details[0]
        timeout = details[1] if len(details) else 0
        return prefix, int(timeout)

    def _exists(self, ara_key):
        """
        Checks if arakoon key exists!
        """
        prefix, _ = self._get_arakoon_key_details(ara_key)
        keys = self.client.prefix(prefix, maxElements=1)

        if len(keys):
            return True

        return False

    def add(self, key, value, timeout=0, version=None):
        ara_key = self._make_arakoon_key(key, timeout=timeout, version=version)

        if self._exists(ara_key):
            return False

        value = self.pickle(value)

        self.client.set(ara_key, value)

        return self.client.exists(ara_key)

    def get(self, key, default=None, version=None):
        ara_key = self._get_arakoon_key(key, version)

        if not ara_key:
            return default
        elif self._is_expired(ara_key):
            if self._auto_delete_expired:
                self.client.delete(ara_key)
            return default

        try:
            val = self.client.get(ara_key)
        except Exception:
            val = default

        return self.unpickle(val)

    def set(self, key, value, timeout=0, version=None):
        old_ara_key = self._get_arakoon_key(key, version)

        # if Key exists, we need to update timestamp
        # So we will create new key, add it, then delete old one!
        # else if Key doesn't exist, we will create a new One!
        ara_key = self._make_arakoon_key(key, timeout=timeout, version=version)

        value = self.pickle(value)

        self.client.set(ara_key, value)

        if self.client.exists(ara_key) and old_ara_key:
            # We can now delete old key
            try:
                self.client.delete(old_ara_key)
            except Exception:
                pass

    def delete(self, key, version=None):
        ara_key = self._get_arakoon_key(key, version)
        if ara_key:
            try:
                self.client.delete(ara_key)
            except Exception:
                pass

    def has_key(self, key, version=None):
        """
        Check if key exists.
        """
        ara_key = self._get_arakoon_key(key, version)
        return ara_key is not None
