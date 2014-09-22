# -*- coding: utf-8 -*-

import copy
import os
import socket
import subprocess
import sys
import time

from .utils import find_executable, get_free_port

POSER_SERVER_BIN = 'poser'
DEFAULT_ARGS = [
]
STARTUP_TIME = 0.4
START_CHECK_ATTEMPTS = 200


class PoserBox(object):
    def __init__(self, poser_bin=None, port=None, scenes_file=None, proxy=None):

        self.poser_bin = poser_bin or find_executable(POSER_SERVER_BIN)
        assert self.poser_bin, (
            'Could not find "{}" in system PATH. Make sure you have Poser '
            'installed.'.format(POSER_SERVER_BIN))

        self.port = port or get_free_port()
        self.scenes_file = scenes_file or os.devnull
        self.proxy = proxy

        self.process = None

    def record(self):
        """Start Poser in Record mode.

        Returns `True` if instance has been started or
        `False` if it could not start.
        """
        args = copy.copy(DEFAULT_ARGS)
        args.insert(0, self.poser_bin)

        args.append('-record')
        args.extend(['-port', str(self.port)])
        args.extend(['-scenes', self.scenes_file])
        args.extend(['-proxy', self.proxy])

        self.process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        return self._wait_till_started()

    def play(self):
        """Start Poser in playback mode.

        Returns `True` if instance has been started or
        `False` if it could not start.
        """
        args = copy.copy(DEFAULT_ARGS)
        args.insert(0, self.poser_bin)

        args.append('-play')
        args.extend(['-port', str(self.port)])
        args.extend(['-scenes', self.scenes_file])

        self.process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        return self._wait_till_started()

    def stop(self):
        if not self.process:
            return

        # Not sure if there should be more checks for
        # other platforms.
        if sys.platform == 'darwin':
            self.process.kill()
        else:
            os.kill(self.process.pid, 9)
        self.process.wait()
        self.process = None

    def running(self):
        return self.process is not None

    def _wait_till_started(self):
        attempts = 0
        while self.process.poll() is None and attempts < START_CHECK_ATTEMPTS:
            attempts += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                try:
                    sock.connect(('localhost', int(self.port)))
                    return True
                except (IOError, socket.error):
                    time.sleep(0.25)
            finally:
                sock.close()

        self.stop()
        return False
