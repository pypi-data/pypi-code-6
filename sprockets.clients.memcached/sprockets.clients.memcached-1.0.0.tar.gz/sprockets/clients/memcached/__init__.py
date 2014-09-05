"""
Memcached Client API
====================
The memcached client API wraps the :py:class:`memcache.Client` adding
environment variable based configuration.

Example environment variable configuration:

    ``<PREFIX>_MEMCACHED_SERVERS = '10.0.0.1:11211:64,10.0.0.2:11211:64'``

"""
import logging
import os

import memcache

version_info = (0, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)

LOGGER = logging.getLogger(__name__)

DEFAULT_SERVER = '127.0.0.1:11211'


def _get_servers(prefix):
    """Return the list of memcached servers from the environment variable
    value, defaulting to ``DEFAULT_SERVER`` if it is not set.

    If prefix is not set, then the environment variable ``MEMCACHED_SERVERS``
    will be be used. If both ``<PREFIX>_MEMCACHED_SERVERS`` and
    ``MEMCACHED_SERVERS`` are not set, the default server value of
    ``127.0.0.1`` will be returned.

    :param str prefix: The environment variable prefix
    :rtype: list

    """
    key = '%s_MEMCACHED_SERVERS' % prefix if prefix else 'MEMCACHED_SERVERS'
    return os.environ.get(key, DEFAULT_SERVER).split(',')


class Client(memcache.Client):
    """Wraps :py:class:`memcache.Client`, passing in the environment
    variable prefix. If prefix is set, the environment variable key is in the
    format ``<PREFIX>_MEMCACHED_SERVERS``. If the prefix is not set, the list
    will attempt to be retrieved from the ``MEMCACHED_SERVERS``. If neither
    environment variable is set, the default value of ``127.0.0.1:11211`` is
    used.

    The per server format in the comma separated list is:

        ``[HOST]:[PORT]<:WEIGHT>``

    Where host and port are required but weight is optional.

    :param str prefix: The environment variable prefix. Default: ``None``

    """
    def __init__(self, prefix=None):
        servers = _get_servers(prefix.upper() if prefix else '')
        LOGGER.debug('Connecting to %r', servers)
        super(Client, self).__init__(servers)
