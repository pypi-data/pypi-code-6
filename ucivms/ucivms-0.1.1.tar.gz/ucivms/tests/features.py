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

import errno
import os
import subprocess


from ucitests import features


qemu_img_feature = features.ExecutableFeature('qemu-img')


class _UseSudoForTestsFeature(features.Feature):
    """User has sudo access.

    There is no direct way to test for sudo access other than trying to use
    it. This is not something we can do in automated tests as it requires user
    input.

    Whatever trick is used to guess whether or not the user *can* sudo won't
    tell us if she agrees to run the sudo tests. Instead, this should rely on
    an opt-in mechanism so each user decides whether or not she wants to run
    the tests.
    """

    def _probe(self):
        # I.e. if you want to run the tests that requires sudo issue:
        # $ touch ~/.uci-vms.use_sudo_for_tests
        # if you don't, issue:
        # $ rm -f ~/.uci-vms.use_sudo_for_tests
        path = os.path.expanduser('~/.uci-vms.use_sudo_for_tests')
        return os.path.exists(path)

    def feature_name(self):
        return 'sudo access'


use_sudo_for_tests_feature = _UseSudoForTestsFeature()


class _SshFeature(features.ExecutableFeature):

    def __init__(self):
        super(_SshFeature, self).__init__('ssh')
        self.version = None

    def _probe(self):
        exists = super(_SshFeature, self)._probe()
        if exists:
            try:
                proc = subprocess.Popen(['ssh', '-V'],
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                out, err = proc.communicate()
            except OSError as e:
                if e.errno == errno.ENOENT:
                    # broken install
                    return False
                else:
                    raise
            self.version = err
        return exists

    def requires_ecdsa(self, test):
        ecdsa_support = 'OpenSSH_5.9p1-5ubuntu.1.1'
        if self.version < ecdsa_support:
            test.skipTest('ecdsa requires ssh >= %s, you have %s'
                          % (ecdsa_support, self.version,))


ssh_feature = _SshFeature()
