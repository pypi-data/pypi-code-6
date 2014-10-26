from testgen import TestGen
from langs import Python


class PythonTester(Python, TestGen):

    basicTest = r"""
# Line Gen:
# g(\d+)_(\d+)
# \g<0> = divmod(\1, \2)

print g9_7
"""

    basicAnswer = r"""
# Line Gen:
# g(\d+)_(\d+)
# \g<0> = divmod(\1, \2)
g9_7 = divmod(9, 7)

print g9_7
"""

    def testBasic(self):
        self.checkGenerates(self.basicTest, self.basicAnswer)

