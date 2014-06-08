from abc import abstractmethod

from plugz import PluginTypeBase

class StandardPluginType(PluginTypeBase):
    """ Simple plugin type that requires an activate() method.

    Plugins that derive from this type will have to implement
    activate() or plugz will refuse to load the plugin.

    The plugintype needs to be set as well. Set it to a string
    that describes the class. It does not have to be the class
    name but it might make things easier for you.

    """

    plugintype = __name__

    @abstractmethod
    def activate(self): pass
