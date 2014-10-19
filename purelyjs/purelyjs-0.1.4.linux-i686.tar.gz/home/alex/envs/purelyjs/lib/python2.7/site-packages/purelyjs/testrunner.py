#!/usr/bin/env python

import logging
import os
import re
import shutil
import tempfile
import time

logging.basicConfig()

from .io import expand_patterns
from .io import write
from .io import writeln
from .interpreter import Interpreter
from .testmodule import TestModule


class TestRunner(object):
    def __init__(self, libs=None, tests=None, interpreters=None,
                 test_name_filter=None,
                 collect_only=False, keep_modules=False, verbose=False):
        self.regexes_test_case = [
            # testSomething
            re.compile('^(?m)function\s+(test[A-Z][A-Z0-9a-z_]+)'),
            # test_something
            re.compile('^(?m)function\s+(test_[^\s()]+)'),
        ]

        purely_pkgroot = os.path.dirname(__file__)
        purely_js = os.path.join(purely_pkgroot, 'js', 'purely.js')

        self.libs = libs or []
        if tests is None:
            raise ValueError("Must provide tests")

        self.libs = expand_patterns(libs + [purely_js])
        self.tests = expand_patterns(tests)
        self.collect_only = collect_only
        self.keep_modules = keep_modules
        self.test_name_filter = test_name_filter
        self.verbose = verbose

        # If we're only collecting then run in verbose mode
        # to display test names
        if self.collect_only:
            self.verbose = True

        self.interpreter = Interpreter(interpreters)

    def find_all_test_cases(self, filepaths):
        test_cases = []

        for filepath in filepaths:
            test_cases.extend(self.find_test_cases(filepath))

        return test_cases

    def find_test_cases(self, filepath):
        with open(filepath, 'rt') as f:
            content = f.read()

        test_cases = []
        for regex in self.regexes_test_case:
            test_cases.extend(regex.findall(content))

        return test_cases

    def check_test_case_uniqueness(self, test_cases):
        dct = {}
        for test_case in test_cases:
            if not test_case in dct:
                dct[test_case] = 0
            dct[test_case] += 1

        for test_case, num in dct.items():
            if num > 1:
                logging.warn("Test case %s defined more than once" % test_case)

    def apply_name_filter(self, test_cases):
        if self.test_name_filter:
            test_cases = [case for case in test_cases
                          if re.search(self.test_name_filter, case)]

        return test_cases

    def run_tests(self, testdir):
        test_cases = self.find_all_test_cases(self.tests)
        self.check_test_case_uniqueness(test_cases)

        test_cases = self.apply_name_filter(test_cases)

        num_tests = len(test_cases)

        writeln('Running %s tests on %s' % (num_tests, self.interpreter.exe))
        t_start = time.time()

        modules = []
        for i, test_case in enumerate(test_cases, 1):
            module = TestModule(
                testdir,
                self.interpreter,
                self.libs + self.tests,
                test_case,
                keep_module=self.keep_modules,
            )
            modules.append((i, module))

            if self.verbose:
                write('%s... ' % module.test_case)

            # If we're just collecting then pretend it passed
            if self.collect_only:
                module.passed = True
            else:
                module.run()

            if module.passed:
                write('.')
            else:
                write('F')

            if self.verbose and not i == num_tests:
                writeln()

        writeln()
        writeln()

        failed_modules = [(i, m) for (i, m) in modules if not m.passed]
        for i, module in failed_modules:
            writeln('=' * 70)
            writeln('FAILED (%s): %s (%s)' %
                    (i, module.test_case, module.filepath))
            writeln('-' * 70)
            writeln(module.stderr)
            writeln()

        writeln('-' * 70)

        t_delta = time.time() - t_start
        writeln('Ran %s tests in %.3fs' % (num_tests, t_delta))

        if failed_modules:
            writeln()
            writeln('FAILED (failed=%s)' % len(failed_modules))
            return False

    def run(self):
        testdir = tempfile.mkdtemp(prefix='purelyjs_testrun_')
        try:
            self.run_tests(testdir)
        finally:
            if not self.keep_modules:
                shutil.rmtree(testdir)
