import unittest
import scanbooker.utils.db
import scanbooker.command.initialise

def suite():
    suites = [
            unittest.makeSuite(InitialiseTest)
        ]
    return unittest.TestSuite(suites)

class InitialiseTest(unittest.TestCase):
    
    def test_setUpTestFixtures(self):
        self.cmd = scanbooker.command.initialise.InitialiseDomainModel()
        self.failUnless(self.cmd)

