from os.path import join, expanduser, dirname
from configparser import ConfigParser
import logging


class Config:
    """
    ``Config.user_ini`` is the location of the user ini file and its default
    value is ``~/.expyrimenter/config.ini``.
    If you change the user config location,
    it will take effect in every new object.
    """
    user_ini = join(expanduser('~'), '.expyrimenter', 'config.ini')
    _default_ini = join(dirname(__file__), 'config.ini')
    _logger = logging.getLogger('config')

    def __init__(self, section):
        """
        :param str section: Ini file section name
        """
        parser = ConfigParser()
        parser.read([Config._default_ini, Config.user_ini])

        if section in parser.sections():
            self._section = parser[section]
        else:
            self._section = {}

    def get(self, key, default=None):
        """
        :param str key: The key whose value you are looking for
        :param any default: value to return if key is not found
        :return: *key* value
        :rtype: str
        """
        return self._section.get(key, default)
