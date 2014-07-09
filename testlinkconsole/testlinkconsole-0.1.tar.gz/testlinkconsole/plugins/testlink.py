from libs.iBDTestPlugin import IBDTestPlugin


class TestlinkPlugin(IBDTestPlugin):

    testlinkclient = ''

    def init(self, apiclient):
        self.testlinkclient = apiclient

    def activate(self):
        super(TestlinkPlugin, self).activate()
        return "Testlink plugin actif"

    def deactivate(self):
        super(TestlinkPlugin, self).deactivate()
        return "Testlink plugin inactif"

    def run(self, browser, script):
        print "Testlink run %s with %s" % (script, browser)

    def listProjects(self):
        result=[]
        for project in self.testlinkclient.getProjects():
            result.append(
                    {
                        'id': project['id'],
                        'name' : project['name'],
                        })
        return result

    def listTestPlans(self, projectid):
        result=[]
        for testplan in self.testlinkclient.getProjectTestPlans(testprojectid=projectid):
            result.append(
                    {
                        'id' : testplan['id'],
                        'name' : testplan['name'],
                        })
        return result

    def listTestCases(self, testplanid):
        result=[]
        for testcase in self.testlinkclient.getTestCasesForTestPlan(testplanid=testplanid):
            result.append(
                    {
                        'id' : testcase['id'],
                        'name' : testcase['name'],
                        })
        return result

