# This file is part of Ubuntu Continuous Integration virtual machine tools.
#
# Copyright 2014 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals

import errno
import os

from ucivms import (
    errors,
    subprocesses,
)


class ConsoleMonitor(object):
    """Monitor a console to identify known events."""

    def __init__(self, stream):
        super(ConsoleMonitor, self).__init__()
        self.stream = stream

    def scan(self):
        while True:
            line = self.stream.readline()
            yield line
            if not line:
                raise errors.ConsoleEOFError()
            elif line.startswith(' * Will now halt'):
                # That's our final_message, we're done
                return
            elif ('Failed loading yaml blob' in line
                  or 'Unhandled non-multipart userdata starting' in line
                  or 'failed to render string to stdout:' in line
                  or 'Failed loading of cloud config' in line):
                raise errors.CloudInitError(line)


def actual_file_size(path):
    """Return file size or None if the file doesn't exist.

    :param path: The file of interest.

    :return: 'path' size or None if the file doesn't exist.
    """
    try:
        stat = os.stat(path)
        return stat.st_size
    except OSError as e:
        if e.errno == errno.ENOENT:
            return None
        else:
            raise


class TailMonitor(ConsoleMonitor):

    def __init__(self, path, offset=None):
        cmd = ['tail', '-F', path]
        # MISSINGTEST
        if offset is not None:
            cmd += ['--bytes', '{}'.format(offset)]
        proc = subprocesses.pipe(cmd)
        super(TailMonitor, self).__init__(proc.stdout)
        self.path = path
        self.cmd = cmd
        self.proc = proc
        self.lines = []

    def scan(self):
        try:
            for line in super(TailMonitor, self).scan():
                # FIXME: Arguably we should decode line from an utf8 encoding
                # as subprocesses.pipe() merges stderr into stdout and utf8
                # error messages have been observed in real life: 'tail: cannot
                # open \xe2\x80\x98/home/vila/vms/lxc1/console\xe2\x80\x99 for
                # reading: Permission denied\n' -- vila 2014-01-19
                self.lines.append(line)
                yield line
        finally:
            self.proc.terminate()
