import os
import sys
import inspect
from collections import defaultdict

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from plugz import PluginTypeBase
import errors


""" Main storage of the plugins."""
_loaded_plugins = defaultdict(list)


def register_plugin(f):
    """ Register the given class as plugin if valid.

    Will be used as decorator in the framework. This function
    also does basic sanity checks in order to reject invalid
    plugins.

    """

    # some basic sanity tests follow
    # ------------------------------
    if not issubclass(f, PluginTypeBase): # make sure that the plugin is of correct type
        logger.warning('%s cannot be registered. It does not inherit from PluginTypeBase.' % f)
        return f

    if f.__abstractmethods__: # make sure all abstract methods have been implemented
        methods = ','.join(f.__abstractmethods__)
        logger.warning('%s cannot be registerd. It has unimplemented abstract methods: %s' % (f, methods))
        return f

    # register the plugin in the system
    _loaded_plugins[getattr(f, 'plugintype', 'unsorted')].append(f)

    # now just return the collable which is a plugin class in this case
    return f


def load_plugins(paths, plugintype):
    """ Load plugins of given type in given directories. """

    # check if the given type is None
    if not plugintype:
        raise errors.NoValidPluginTypeError()

    # check if the given PluginType really is a subclass
    # of the provided PluginTypeBase
    elif not issubclass(plugintype, PluginTypeBase):
        raise errors.InvalidPluginTypeError()

    # if no paths are given, complain.
    elif not paths:
        raise errors.NoPluginPathsProvided()

    # if an invalid path is given, report that problem
    else:
        for path in paths:
            if not os.path.isdir(path):
                raise errors.InvalidPluginPath()

    # we need to clear plugins that were loaded before
    del _loaded_plugins[plugintype.plugintype][:]

    # otherwise all data is valid for loading some plugins
    for path in paths:
        # find all the files and try to register them as plugins
        sys.path.insert(0, path)
        for pf in os.listdir(path):
            if plugintype.is_valid_file(pf):
                # as long as only files with extensions are used, this works.
                base = os.path.basename(pf).split(os.path.extsep)[0]
                _load_plugin(base)

        sys.path.pop(0)

    return _loaded_plugins[plugintype.plugintype]


def _load_plugin(plugin_name):
    logger.debug('Loading %s...' % plugin_name)
    p = __import__(plugin_name)
