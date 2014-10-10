# Copyright (c) 2010 Florian Friesdorf <flo@chaoflow.net>
# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import logging
import restarter
import restarter.proc
import subprocess
import time


class Service:
    """Represents a system service."""

    def __init__(self, proc, restart_cmd=None, hard_restart_cmd=None, delay=0):
        self.proc = proc
        self.restart_cmd = restart_cmd
        self.hard_restart_cmd = hard_restart_cmd
        self.delay = delay
        self.restart_pending = False
        self.log = logging.getLogger('restarter')

    def check_restart(self):
        """Determine if a restart is necessary and perform it."""
        self.restart_pending = self.proc.stale
        if self.restart_pending:
            self.restart()

    def restart(self):
        """Perform service restart if restart_cmd is defined.

        If restart_cmd does not have the desired effect and hard_restart_cmd is
        defined, take one more attempt but fail if that does not help, too.
        """

        if self.restart_cmd:
            try:
                self._restart_verify(self.restart_cmd)
            except restarter.RestartError as e:
                if self.hard_restart_cmd:
                    self.log.warning(str(e))
                    self._restart_verify(self.hard_restart_cmd)
                else:
                    raise
            self.restart_pending = False

    def _restart_verify(self, cmd):
        """Handle low-level service restart.

        A restart command is executed and the process is checked. Verify that
        the service is actually running and that the new process is different
        from the old one.
        """

        self.log.info('trying to restart using {}'.format(cmd))
        with open('/dev/null', 'rb') as null:
            rc = subprocess.call(cmd, shell=True, stdin=null)
        if rc != 0:
            raise restarter.RestartError(
                'command "{}" was not successful (exit status {})'.format(
                    cmd, rc))
        time.sleep(self.delay)
        try:
            newproc = self.proc.reread()
        except restarter.PidfileError:
            raise restarter.RestartError(
                'failed, no new service pid found for {}'.format(
                    self.proc.pidfile))
        if newproc == self.proc:
            raise restarter.RestartError(
                'failed, old process {} is still running'.format(
                    self.proc.pid))
