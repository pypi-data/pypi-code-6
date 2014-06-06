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

import subprocess


from ucivms import (
    errors,
)


def run(args):
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        raise errors.CommandError(args, proc.returncode, out, err)
    return proc.returncode, out, err


def pipe(args):
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc


# MISSINGTEST
def ssh(user, host, command, *args):
    cmd = ['ssh', '{}@{}'.format(user, host)]
    if command is not None:
        cmd += [command]
        if args:
            cmd += args
    proc = subprocess.Popen(cmd)
    out, err = proc.communicate()
    return proc
