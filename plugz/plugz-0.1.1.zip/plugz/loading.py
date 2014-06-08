import os
import sys
import inspect
from collections import defaultdict

from plugz import PluginTypeBase
import errors

_loaded_plugins = defaultdict(list)

def register_plugin(f):
    """

    will be used as decorator
    """

    # TODO, logging!!

    # some basic sanity tests follow
    if not issubclass(f, PluginTypeBase): # make sure that the plugin is of correct type
        print 'Warning: %s cannot be registered because it does not inherit from PluginTypeBase.' % f
        return f

    if f.__abstractmethods__: # make sure all abstract methods have been implemented
        print 'Warning: %s cannot be registerd because it has unimplemented abstract methods: %s' % (f,  [x for x in f.__abstractmethods__])
        return f

    # register the plugin in the system
    _loaded_plugins[getattr(f, 'plugintype', 'unsorted')].append(f)

    # now just return the collable which is a plugin class in this case
    return f


def load_plugins(paths, plugintype):
    """
    """
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
    # TODO, make this proper logged stuff. -- Matti.
    p = __import__(plugin_name)
