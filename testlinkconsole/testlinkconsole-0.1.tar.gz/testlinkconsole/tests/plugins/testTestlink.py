import unittest
import mock
import mox

from plugins.testlink import TestlinkPlugin
from testlink import TestlinkAPIClient

class TestingClassTestlinkAPIClient(TestlinkAPIClient):
    def __init__(self, server_url,  devkey):
        super(TestingClassTestlinkAPIClient, self).__init__(server_url, devkey)


class TestTestlinkPlugin(unittest.TestCase):

    def setUp(self):
        self.mocker = mox.Mox()
        self.apiclient = self.mocker.CreateMock(TestingClassTestlinkAPIClient)
        self.plugin = TestlinkPlugin()
        self.plugin.init(self.apiclient)

    def test_activate(self):
        self.assertEquals(self.plugin.activate(), "Testlink plugin actif")

    def test_deactivate(self):
        self.assertEquals(self.plugin.deactivate(), "Testlink plugin inactif")

    @mock.patch('__builtin__.print')
    def test_run(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.plugin.run('profile','script'),None)

    def test_listProjects(self):
        projectsIn=[
                {'id':'1', 'name':'projet1', 'description':'description1'},
                {'id':'2', 'name':'projet2', 'description':'description2'},
                ]
        projectsOut=[
                {'id':'1', 'name':'projet1'},
                {'id':'2', 'name':'projet2'},
                ]
        self.apiclient.getProjects().AndReturn(projectsIn)
        self.mocker.ReplayAll()
        self.assertEquals(self.plugin.listProjects(),projectsOut)

    def test_listTestPlans(self):
        testPlansIn=[
                {'id':'1', 'name':'campagne1', 'description':'description1'},
                    ]
        testPlansOut=[
                {'id':'1', 'name':'campagne1'},
                    ]
        self.apiclient.getProjectTestPlans(testprojectid=1).AndReturn(testPlansIn)
        self.mocker.ReplayAll()
        self.assertEquals(self.plugin.listTestPlans(1), testPlansOut)

    def test_listTestCases(self):
        testCasesIn=[
                {'id':'1', 'name':'test1', 'description':'description du test 1'},
                ]
        testCasesOut=[
                {'id':'1', 'name':'test1'},
                ]
        self.apiclient.getTestCasesForTestPlan(testplanid=1).AndReturn(testCasesIn)
        self.mocker.ReplayAll()
        self.assertEquals(self.plugin.listTestCases(1), testCasesOut)

    @unittest.skip('TODO')
    def test_getInfoProject(self):
        pass

    @unittest.skip('TODO')
    def test_getInfoTestPlan(self):
        pass

    @unittest.skip('TODO')
    def test_getInfoTestCase(self):
        pass

    @unittest.skip('TODO')
    def test_runTestPlan(self):
        pass

    @unittest.skip('TODO')
    def test_runTestCase(self):
        pass

if __name__ == '__main__':
    unittest.main()
