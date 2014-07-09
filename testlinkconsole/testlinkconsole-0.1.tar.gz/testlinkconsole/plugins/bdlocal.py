from libs.iBDTestPlugin import IBDTestPlugin

class BDLocalPlugin(IBDTestPlugin):
    def __init__(self):
        super(BDLocalPlugin,self).__init__()
        # add command to console : TODO
        #setattr(self.app.__class__,'do_createlocal',classmethod(self.do_createlocal))
        #setattr(self.app.__class__,'help_createlocal',classmethod(self.help_createlocal))

    def activate(self):
        super(BDLocalPlugin, self).activate()
        return "BDLocal plugin actif"

    def deactivate(self):
        super(BDLocalPlugin, self).deactivate()
        return "BDLocal plugin inactif"

    def run(self, browser, script):
        print "BDLocal run %s with %s" % (script, browser)

    @staticmethod
    def do_createlocal(self,line ):
        print "Bonjour du plugins"

    @staticmethod
    def help_createlocal(self):
        print '\n'.join([' createlocal plugins',
                         'juste un test pour le fun'
                         ])
