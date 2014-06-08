import abc

class PluginTypeBase(object):
    """ Baseclass for plugin types.

    This needs to be derived from in order for plugin types to
    be accepted by plugz.

    """
    __metaclass__ = abc.ABCMeta

    plugintype = None

    @staticmethod
    def is_valid_file(file):
        """ Accept or reject files as valid plugins. """
        return file.endswith('.py')
