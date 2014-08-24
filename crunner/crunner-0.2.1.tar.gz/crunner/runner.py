# -*- coding: utf-8 -*-
import os
import time

from subprocess import Popen
from .logger import log


class Runner(object):
    def __init__(self, notifier, tester_cmd, tester_args):
        self._tester_cmd = tester_cmd
        self._tester_args = tester_args
        self._notifier = notifier

    def test(self, name, project_path, test_path):
        self._print_execution_header()
        result = self._execute_tests(project_path, test_path)
        self._call_notifier(name, result)

    def _print_execution_header(self):
        log.info(
            "\n\n\n" +
            "".ljust(40, '-').rjust(80, '-') +
            "\n{}\n".format('PYTEST EXECUTION'.ljust(40).rjust(80)) +
            "".ljust(40, '-').rjust(80, '-') +
            "\n\n\n"
        )

    def _execute_tests(self, project_path, test_path="2222"):
        if not os.path.exists(project_path):
            log.warn("Specified path ({}) doesn't exist. Tests are skipped.".format(project_path))
            return -1
        os.chdir(project_path)
        cmd = "cd {}; {} {} {}".format(project_path, self._tester_cmd, self._tester_args, test_path)
        proc = Popen(cmd, shell=True)
        return self._wait_until_execution_result(proc)

    def _wait_until_execution_result(self, proc):
        result = None
        while result is None:
            result = proc.poll()
            time.sleep(.1)
        return result

    def _call_notifier(self, name, result):
        if result == 0:
            self._notifier.send_ok(name)
        else:
            self._notifier.send_nok(name)
