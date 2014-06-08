import plugz

@plugz.register_plugin
class MyValidPluginTwo(plugz.StandardPluginType):
    """ Basic plugin for tests.

    Inherit from StandardPluginType and implement activate().
    """

    def __init__(self, ):
        """ """
        # do all your initialization here
        pass

    def activate(self):
        """ """
        pass
