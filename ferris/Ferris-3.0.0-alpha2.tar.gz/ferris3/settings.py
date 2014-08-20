from __future__ import absolute_import
import logging

_defaults = {}


class ConfigurationError(Exception):
    pass


def load(refresh=False):
    """
    Executed when the project is created and loads the settings from app/settings.py
    """
    global _defaults

    if _defaults and not refresh:
        return

    try:
        import app.settings as appsettings
        reload(appsettings)
    except ImportError:
        raise ConfigurationError("Settings not found. Please create app/settings.py")

    try:
        appdefaults = appsettings.settings
    except AttributeError:
        raise ConfigurationError("No dictionary 'settings' found in settings.py")

    logging.info("Ferris settings loaded")

    defaults(appdefaults)


def defaults(dict=None):
    """
    Adds a set of default values to the settings registry. These can and will be updated
    by any settings modules in effect, such as the Settings Manager.

    If dict is None, it'll return the current defaults.
    """
    if dict:
        _defaults.update(dict)
    else:
        return _defaults


def all():
    """
    Returns the entire settings registry
    """
    settings = {}
    settings.update(_defaults)
    return settings


def set(key, value):
    global _defaults
    _defaults[key] = value


def get(key, default=None):
    """
    Returns the setting at key, if available, raises an ConfigurationError if default is none, otherwise
    returns the default
    """
    _settings = all()
    if key not in _settings:
        if default is None:
            raise ConfigurationError("Missing setting %s" % key)
        else:
            return default
    return _settings[key]
