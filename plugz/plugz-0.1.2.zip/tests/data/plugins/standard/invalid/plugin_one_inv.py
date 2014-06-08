import plugz

print plugz

@plugz.register_plugin
class MyInvalidPluginOne(plugz.StandardPluginType):
    """ Basic plugin for tests.

    Inherit from StandardPluginType and don't implement activate().
    """

    def __init__(self, ):
        """ """
        pass

    # def activate(self):
    #     """ """
    #     print 'activating %s' % __name__
