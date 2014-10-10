# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import logging
import os
import restarter
import restarter.service
import restarter.proc


class App:
    """Main application skeleton."""

    def __init__(self, pidfile, options):
        """Set up program parameters."""
        self.pidfile = pidfile
        self.restart_cmd = options.restart
        self.hard_restart_cmd = options.hard_restart
        self.delay = options.delay
        self.fail = options.fail
        self.exclude = options.exclude
        self.perform_restart = False
        self.log = logging.getLogger('restarter')
        self.log.setLevel(logging.DEBUG)

    def __call__(self):
        """Perform program run."""
        try:
            proc = restarter.proc.readpid(self.pidfile, self.exclude)
        except restarter.PidfileError as e:
            if self.fail:
                raise restarter.RestartError(str(e))
            return
        svc = restarter.service.Service(
            proc, self.restart_cmd, self.hard_restart_cmd, self.delay)
        svc.check_restart()
        return svc.restart_pending
