from libs.iRunnerPlugin import IRunnerPlugin

class BehavePlugin(IRunnerPlugin):
    def activate(self):
        super(BehavePlugin, self).activate()
        return "Behave plugin actif"

    def deactivate(self):
        super(BehavePlugin, self).deactivate()
        return "Behave plugin inactif"

    def run(self, browser, script):
        print "Behave run %s with %s" % (script, browser)
