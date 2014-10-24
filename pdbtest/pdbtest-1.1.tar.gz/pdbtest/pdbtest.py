# Copyright 2014 Zachary J. McCord
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# and a copy of the license is also included in this software package.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

"""
A simple library to be used after the manner of unittest that tries to hook
test suites and make them invoke PDB on exceptions. For the situation where you
don't really have control over the test code, or don't want to modifiy the test
code, but still want to get an interactive debugger instead of a summary.
"""

from __future__ import print_function
import unittest
import pdb
import types
import sys


def pdb_wrap(fun, message=None):
    "Wrap a function to invoke PDB on exception"
    def hooked_fun(*args, **kwargs):
        "Hooked version of the given function"
        try:
            fun(*args, **kwargs)
        except:
            exc_info = sys.exc_info()
            if message is not None:
                print(message, file=sys.stderr)
            print(exc_info[1], file=sys.stderr)
            pdb.post_mortem(exc_info[2])
    return hooked_fun


def pdb_wrap_cases(test):
    "Wrap a test case or test suite to invoke PDB on exception"
    if hasattr(test, '_tests'):
        # print("Wrapping suite", test, file=sys.stderr)
        for i in xrange(len(test._tests)):
            test._tests[i] = pdb_wrap_cases(test._tests[i])
    else:
        # print("Wrapping test", test, file=sys.stderr)
        testMethod = getattr(test, test._testMethodName)

        def doc_line(docstring):
            return "\n'" + docstring.strip() + "'" if docstring else ''

        message = "Debugging exception in test %r%s\nmethod %r%s" % (
            type(test), doc_line(test.__doc__),
            test._testMethodName, doc_line(testMethod.__doc__))
        setattr(test, test._testMethodName, pdb_wrap(testMethod, message))

    return test


class PDBRunnerMixin(object):
    """
    Mixin class that makes a unittest runner open PDB postmortem on exceptions
    in tests
    """
    def run(self, test):
        "Wrap the test case with PDB catch-debug and then run as normal"
        hooked_test = pdb_wrap_cases(test)
        return super(PDBRunnerMixin, self).run(hooked_test)


class TestProgram(unittest.TestProgram):
    """
    Subclass of unittest main that uses PDBRunnerMixin
    """

    def __init__(self,
                 module=None,
                 testRunner=unittest.TextTestRunner,
                 *args, **kwargs):
        """
        Take the specified testRunner, mix in the PDB behavior, and continue
        like normal
        """
        assert isinstance(testRunner, types.TypeType)
        testRunner = type("PDB" + testRunner.__name__,
                          (PDBRunnerMixin, testRunner),
                          dict())
        # pdb.set_trace()
        super(TestProgram, self).__init__(*args,
                                          testRunner=testRunner,
                                          module=module,
                                          **kwargs)


main = TestProgram
