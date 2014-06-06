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

import os
import unittest

from uciconfig import errors
from ucivms import (
    config,
    vms,
)
from ucivms.tests import fixtures


class TestVmMatcher(unittest.TestCase):

    def setUp(self):
        super(TestVmMatcher, self).setUp()
        fixtures.isolate_from_disk(self)
        self.store = config.VmStore('foo.conf')
        self.matcher = config.VmMatcher(self.store, 'test')

    def test_empty_section_always_matches(self):
        self.store._load_from_string('foo=bar')
        matching = list(self.matcher.get_sections())
        self.assertEqual(1, len(matching))

    def test_specific_before_generic(self):
        self.store._load_from_string('foo=bar\n[test]\nfoo=baz')
        matching = list(self.matcher.get_sections())
        self.assertEqual(2, len(matching))
        # First matching section is for test
        self.assertEqual(self.store, matching[0][0])
        base_section = matching[0][1]
        self.assertEqual('test', base_section.id)
        # Second matching section is the no-name one
        self.assertEqual(self.store, matching[0][0])
        no_name_section = matching[1][1]
        self.assertIs(None, no_name_section.id)


class TestVmStackOrdering(unittest.TestCase):

    def setUp(self):
        super(TestVmStackOrdering, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')

    def test_default_in_empty_stack(self):
        self.assertEqual('1024', self.conf.get('vm.ram_size'))

    def test_system_overrides_internal(self):
        self.conf.system_store._load_from_string('vm.ram_size = 42')
        self.assertEqual('42', self.conf.get('vm.ram_size'))

    def test_user_overrides_system(self):
        self.conf.system_store._load_from_string('vm.ram_size = 42')
        self.conf.store._load_from_string('vm.ram_size = 84')
        self.assertEqual('84', self.conf.get('vm.ram_size'))

    def test_local_overrides_user(self):
        self.conf.system_store._load_from_string('vm.ram_size = 42')
        self.conf.store._load_from_string('vm.ram_size = 84')
        self.conf.local_store._load_from_string('vm.ram_size = 168')
        self.assertEqual('168', self.conf.get('vm.ram_size'))


class TestVmStack(unittest.TestCase):
    """Test config option values."""

    def setUp(self):
        super(TestVmStack, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.conf.store._load_from_string('''
vm.release=raring
vm.cpu_model=amd64
''')

    def assertValue(self, expected_value, option):
        self.assertEqual(expected_value, self.conf.get(option))

    def test_raring_iso_url(self):
        self.assertValue('http://cdimage.ubuntu.com/daily-live/current/',
                         'vm.iso_url')

    def test_raring_iso_name(self):
        self.assertValue('raring-desktop-amd64.iso', 'vm.iso_name')

    def test_raring_cloud_image_url(self):
        self.assertValue('http://cloud-images.ubuntu.com/raring/current/',
                         'vm.cloud_image_url')

    def test_raring_cloud_image_name(self):
        self.assertValue('raring-server-cloudimg-amd64-disk1.img',
                         'vm.cloud_image_name')

    def test_apt_proxy_set(self):
        proxy = 'apt_proxy: http://example.org:4321'
        self.conf.set('vm.apt_proxy', proxy)
        self.conf.store.save_changes()
        self.assertEqual(proxy, self.conf.expand_options('{vm.apt_proxy}'))

    def test_download_cache_with_user_expansion(self):
        download_cache = '~/installers'
        self.conf.set('vm.download_cache', download_cache)
        self.conf.store.save_changes()
        self.assertValue(os.path.join(self.home_dir, 'installers'),
                         'vm.download_cache')

    def test_images_dir_with_user_expansion(self):
        images_dir = '~/images'
        self.conf.set('vm.images_dir', images_dir)
        self.conf.store.save_changes()
        self.assertValue(os.path.join(self.home_dir, 'images'),
                         'vm.images_dir')


class TestPathOption(unittest.TestCase):

    def setUp(self):
        super(TestPathOption, self).setUp()
        fixtures.isolate_from_disk(self)

    def assertConverted(self, expected, value):
        option = config.PathOption('foo', help_string='A path.')
        self.assertEquals(expected, option.convert_from_unicode(None, value))

    def test_absolute_path(self):
        self.assertConverted('/test/path', '/test/path')

    def test_home_path_with_expansion(self):
        self.assertConverted(self.home_dir, '~')

    def test_path_in_home_with_expansion(self):
        self.assertConverted(os.path.join(self.home_dir, 'test/path'),
                             '~/test/path')


class TestVmClass(unittest.TestCase):

    def setUp(self):
        super(TestVmClass, self).setUp()
        fixtures.isolate_from_disk(self)

    def test_class_mandatory(self):
        conf = config.VmStack('I-dont-exist')
        with self.assertRaises(errors.OptionMandatoryValueError):
            conf.get('vm.class')

    def test_lxc(self):
        conf = config.VmStack('I-dont-exist')
        conf.store._load_from_string('''vm.class=lxc''')
        self.assertIs(vms.Lxc, conf.get('vm.class'))

    def test_kvm(self):
        conf = config.VmStack('I-dont-exist')
        conf.store._load_from_string('''vm.class=kvm''')
        self.assertIs(vms.Kvm, conf.get('vm.class'))

    def test_bogus(self):
        conf = config.VmStack('I-dont-exist')
        conf.store._load_from_string('''vm.class=bogus''')
        with self.assertRaises(errors.OptionMandatoryValueError):
            conf.get('vm.class')
