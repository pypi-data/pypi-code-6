# -*- coding: utf-8 -*-
# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import time
import psutil

from cubicweb import ValidationError
from cubes.subprocess.entities import Subprocess
from cubes.subprocess.error import ProcessNotRunning

from utils import SubprocessTC


class SubprocessEntityTC(SubprocessTC):
    def check_subprocess_status(self, retcode, expected_state):
        '''Start a subprocess that returns with ``retcode``.
        Check the db for recorded return code and workflow state.'''
        cmd = 'import sys; sys.exit(%d)' % retcode
        with self.admin_access.client_cnx() as cnx:
            subprocess = self.pyprocess(cnx, cmd)
            self.fire_transition(subprocess, 'start')
            self.wait_finished(subprocess)
            subprocess.cw_clear_all_caches()
            self.assertEqual(retcode, subprocess.return_code)
            effective_state = subprocess.cw_adapt_to('IWorkflowable').state
            self.assertEqual(expected_state, effective_state)

    def test_start(self):
        with self.admin_access.repo_cnx() as cnx:
            subprocess = self.pyprocess(cnx, 'pass')
            self.fire_transition(subprocess, 'start')
            self.wait_finished(subprocess)
            self.assertEqual(0, subprocess.return_code)

    def test_start_and_succeeds(self):
        self.check_subprocess_status(retcode=0, expected_state=u'succeeded')

    def test_start_and_fails(self):
        '''what ?!? The answer of the universe is expected as a failure :/'''
        self.check_subprocess_status(retcode=42, expected_state=u'failed')

    def test_start_fails_outside_workflow(self):
        with self.admin_access.repo_cnx() as cnx:
            subprocess = self.pyprocess(cnx, 'pass')
            self.assertRaises(AssertionError, subprocess.start)

    def test_kill_running(self):
        with self.admin_access.repo_cnx() as cnx:
            subprocess = self.pyprocess(cnx, 'import time; time.sleep(3600);')
            starttime = time.time()
            self.fire_transition(subprocess, 'start')
            self.wait_started(subprocess)

        with self.admin_access.repo_cnx() as cnx:
            subprocess = cnx.entity_from_eid(subprocess.eid)
            subprocess.kill()
            self.assertLess(time.time() - starttime, 3599) # must be killed quickly
            self.wait_finished(subprocess, 2)
            self.assertFalse(psutil.pid_exists(subprocess.pid))

    def test_kill_finished(self):
        with self.admin_access.repo_cnx() as cnx:
            subprocess = self.pyprocess(cnx, 'pass')
            self.fire_transition(subprocess, 'start')
            self.wait_finished(subprocess)
            self.assertRaises(ValidationError, self.fire_transition, subprocess, 'kill')

    def test_kill_not_running(self):
        with self.admin_access.repo_cnx() as cnx:
            subprocess = self.pyprocess(cnx, 'import time; time.sleep(3600);')
            self.fire_transition(subprocess, 'start', deny_hooks='subprocess.workflow')
            self.assertRaises(ProcessNotRunning, subprocess.kill)

    def test_kill_fails_outside_workflow(self):
        with self.admin_access.repo_cnx() as cnx:
            subprocess = self.pyprocess(cnx, 'import time; time.sleep(3600);')
            self.assertRaises(ValidationError, subprocess.kill)

    def test_stdout_stderr(self):
        with self.admin_access.repo_cnx() as cnx:
            pycode = 'print "toto" * 1000; raise ValueError("tutu")'
            subprocess = self.pyprocess(cnx, pycode)
            self.fire_transition(subprocess, 'start')
            self.wait_finished(subprocess)
            subprocess.cw_clear_all_caches()
            efiles = cnx.find('File', output_of=subprocess.eid)
            self.assertEqual(2, len(efiles))
            expecteds = {'stdout': 'toto' * 1000 + '\n',
                         'stderr': '''Traceback (most recent call last):
  File "<string>", line 1, in <module>
ValueError: tutu
'''}
            for efile in efiles.entities():
                self.assertEqual(expecteds[efile.data_name], efile.data.getvalue())


if __name__ == '__main__':
    import unittest
    unittest.main()
