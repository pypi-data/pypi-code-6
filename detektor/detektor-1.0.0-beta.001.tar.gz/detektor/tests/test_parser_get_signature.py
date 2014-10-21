import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detektor.libs.codeparser import Parser


class GetParserGetSignature(unittest.TestCase):

    def setUp(self):
        self.testfilehandler = open('detektor/tests/pyfiles/helloworldplus.py', 'r')
        p = Parser('python', self.testfilehandler)
        self.detektor_signature = p.get_code_signature()

    def tearDown(self):
        self.testfilehandler.close()

    def testGetPythonContentFileSignature(self):
        self.assertEqual(type(self.detektor_signature), dict)

    def testGetPythonContentFileSignatureHasBigstring(self):
        self.assertTrue('bigstring' in self.detektor_signature)

    def testGetPythonContentFileSignatureHasKeywordstring(self):
        self.assertTrue('keywordstring' in self.detektor_signature)

    def testGetPythonContentFileSignatureHasOperatorstring(self):
        self.assertTrue('operatorstring' in self.detektor_signature)

    def testGetPythonContentFileSignatureHasBigstringhash(self):
        self.assertTrue('bigstringhash' in self.detektor_signature)

    def testGetPythonContentFileSignatureHaslist_of_functions(self):
        self.assertTrue('list_of_functions' in self.detektor_signature)

    def testGetPythonContentFileSignatureHasnumber_of_keywords(self):
        self.assertTrue('number_of_keywords' in self.detektor_signature)

    def testGetPythonContentFileSignatureHasnumber_of_operators(self):
        self.assertTrue('number_of_operators' in self.detektor_signature)
