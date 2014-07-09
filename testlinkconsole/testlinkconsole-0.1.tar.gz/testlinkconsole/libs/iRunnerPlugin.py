from yapsy.IPlugin import IPlugin

class IRunnerPlugin(IPlugin):

    def activate(self):
        super(IRunnerPlugin, self).activate()
        return "IRunnerPlugin actif"

    def deactivate(self):
        super(IRunnerPlugin, self).deactivate()
        return "IRunnerPlugin inactif"
