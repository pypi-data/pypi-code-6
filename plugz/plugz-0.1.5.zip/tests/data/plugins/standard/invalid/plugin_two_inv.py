import plugz

@plugz.register_plugin
class MyInvalidPluginTwo(object):
    """ Basic plugin for tests.

    Inherit from object and implement activate().
    """

    def __init__(self, ):
        """
        """
        pass

    def activate(self):
        """ """
        print 'activating %s' % __name__
