from jinja2 import Template
import sys


class TestGenerator(object):

    def gen(self, tests=[]):
        template = Template("""#!/usr/bin/env python
import difflib
import unittest
import shlex, subprocess
import os

class TestScript(unittest.TestCase):

    def setUp(self):
        self.base = ['python', '{{ script_name }}']
        self.tests = {{ tests }}
    def test_run(self):
        for test_case in self.tests:
            failed_test = False
            try:
                current_command = self.base + \\
                    shlex.split(test_case['command_line'])
                # Should probably be wrapped in an assert as well
                subprocess.check_call(current_command)

                for fileset in test_case['outputs']:
                    failed_test = self.file_comparison(
                            test_case['outputs'][fileset][0],
                            test_case['outputs'][fileset][1])
            except:
                raise
            self.assertFalse(failed_test)

    def file_comparison(self, test_file, comp_file):
        failed_test = False
        diff=difflib.unified_diff(open(test_file).readlines(),
                           open(comp_file).readlines())
        try:
            while True:
                print diff.next(),
                failed_test = True
        except:
            pass
        try:
            # Attempt to remove the generated file to cut down on
            # clutter/other bad things
            os.unlink(test_file)
        except:
            pass
        return failed_test

if __name__ == '__main__':
    unittest.main()
""")
        # For all the tests, we need to remove params in lieu of generated command line
        for test in tests:
            # Generate the command line
            cli = ""
            for param in test['params']:
                # Assume long option. Possibly bad?
                cli += '--' + param + " " + test['params'][param]
            # Remove params when done
            try:
                del test['params']
            except:
                pass
            test['command_line'] = cli

        return template.render({'tests': tests, 'script_name': sys.argv[0]})
