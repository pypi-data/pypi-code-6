import abc

class PluginTypeBase(object):

    __metaclass__ = abc.ABCMeta

    plugintype = None

    @staticmethod
    def is_valid_file(file):
        """ """
        return file.endswith('.py')
