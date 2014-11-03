from os.path import join, expanduser, dirname
from configparser import ConfigParser
import logging


class Config:
    """Consider the following expyrimenter.ini:
    [my_section]
    var1 = one

    >>> from expyrimenter import Config
    >>> config = Config('my_section')
    >>> config.get('var1')
    'one'
    >>> config.get('var2', 'default_value')
    default_value
    >>> config.get('var2') is None
    True
    """
    user_ini = join(expanduser('~'), '.expyrimenter', 'config.ini')
    _default_ini = join(dirname(__file__), 'config.ini')
    _logger = logging.getLogger('config')

    def __init__(self, section):
        parser = ConfigParser()
        parser.read([Config._default_ini, Config.user_ini])

        if section in parser.sections():
            self._section = parser[section]
        else:
            self._section = {}

    def get(self, key, default=None):
        return self._section.get(key, default)
