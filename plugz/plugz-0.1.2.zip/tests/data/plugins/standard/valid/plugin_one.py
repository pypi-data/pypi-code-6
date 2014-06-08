import plugz

@plugz.register_plugin
class MyFirstValidPlugin(plugz.StandardPluginType):
    """ Basic plugin to show as an example.

    Inherit from StandardPluginType and implement activate(). If
    activate is not implemented here, plugz would refuse to load the
    plugin.

    """

    def __init__(self, ):
        """ Initialize the plugin.

        You can copy files, request database entries or do other preprocessing
        here. Usually, the host will only hold one instance of this class
        but it could equally as well create multiple, if it needs to for some reason.

        """
        pass

    def activate(self):
        """ Activate the plugin.

        You can require a licence here or do other things that are necessary
        to get this plugin up and running.

        """
        print __name__, 'has just been activated!'
