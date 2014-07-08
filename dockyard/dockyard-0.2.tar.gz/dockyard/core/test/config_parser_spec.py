import unittest
import lib

class TestSequenceFunctions(unittest.TestCase):


    def setUp(self):
        pass

    def test_shuffle(self):

        jsonConfig = '''
            {
                "domain": {
                    "tld": "webstack.com",
                    "dns": [
                        "172.17.42.1",
                        "8.8.8.8",
                        "8.8.4.4"
                    ],
                    "dockyards": {
                        "wildfly-cluster": {
                        }
                    }
                }
            }
        '''

        configParser = lib.ConfigParser()
        configParser.parse(jsonConfig)




if __name__ == '__main__':
    unittest.main()