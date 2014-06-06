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

import os
import unittest

from ucitests import features

from ucivms import ssh
from ucivms.tests import (
    features as vms_features,
    fixtures as vms_fixtures,
)


class TestInfoFromPath(unittest.TestCase):

    def assertInfo(self, expected, key_path):
        self.assertEqual(expected, ssh.infos_from_path(key_path))

    # FIXME: This is screaming parametrization !!! But we don't have scenarios
    # yet -- vila 2014-01-16

    def test_public_rsa(self):
        self.assertInfo(('rsa', 'public'), './rsa.pub')

    def test_private_rsa(self):
        self.assertInfo(('rsa', 'private'), './rsa')

    def test_public_dsa(self):
        self.assertInfo(('dsa', 'public'), './dsa.pub')

    def test_private_dsa(self):
        self.assertInfo(('dsa', 'private'), './dsa')

    def test_public_ecdsa(self):
        self.assertInfo(('ecdsa', 'public'), './ecdsa.pub')

    def test_private_ecdsa(self):
        self.assertInfo(('ecdsa', 'private'), './ecdsa')

    def test_unknown(self):
        self.assertInfo((None, 'public'), './foo.pub')
        self.assertInfo((None, 'private'), './foo')


@features.requires(vms_features.ssh_feature)
class TestKeyGen(unittest.TestCase):

    def setUp(self):
        super(TestKeyGen, self).setUp()
        vms_fixtures.isolate_from_disk(self)

    def keygen(self, ssh_type, upper_type=None):
        if upper_type is None:
            upper_type = ssh_type.upper()
        private_path = os.path.join(self.uniq_dir, ssh_type)
        ssh.keygen(private_path, 'uci-vms@test')
        self.assertTrue(os.path.exists(private_path))
        public_path = private_path + '.pub'
        self.assertTrue(os.path.exists(public_path))
        public = file(public_path).read()
        private = file(private_path).read()
        self.assertTrue(
            private.startswith('-----BEGIN %s PRIVATE KEY-----\n'
                               % (upper_type,)))
        self.assertTrue(
            private.endswith('-----END %s PRIVATE KEY-----\n' % (upper_type,)))
        self.assertTrue(public.endswith(' uci-vms@test\n'))
        return private, public

    def test_dsa(self):
        private, public = self.keygen('dsa')
        self.assertTrue(public.startswith('ssh-dss '))

    def test_rsa(self):
        private, public = self.keygen('rsa')
        self.assertTrue(public.startswith('ssh-rsa '))

    def test_ecdsa(self):
        vms_features.ssh_feature.requires_ecdsa(self)
        private, public = self.keygen('ecdsa', 'EC')
        self.assertTrue(public.startswith('ecdsa-sha2-nistp256 '))
