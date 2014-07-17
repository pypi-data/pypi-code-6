from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton

class IBDTestPlugin(IPlugin):

    def __init__(self):
        #manager = PluginManagerSingleton.get()
        #self.app = manager.app
        super(IBDTestPlugin,self).__init__()

    def activate(self):
        super(IBDTestPlugin, self).activate()
        return "IBDTestPlugin actif"

    def deactivate(self):
        super(IBDTestPlugin, self).deactivate()
        return "IBDTestPlugin inactif"
