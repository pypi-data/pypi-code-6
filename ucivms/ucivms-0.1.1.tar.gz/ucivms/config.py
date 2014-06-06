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

from uciconfig import (
    options,
    registries,
    stacks,
    stores,
)


class VmMatcher(stacks.NameMatcher):

    def match(self, section):
        if section.id is None:
            # The no name section contains default values
            return True
        return super(VmMatcher, self).match(section)

    def get_sections(self):
        matching_sections = super(VmMatcher, self).get_sections()
        return reversed(list(matching_sections))


VmStore = stores.FileStore


def system_config_dir():
    return '/etc'


class VmStack(stacks.Stack):
    """Per-directory options."""

    def __init__(self, name):
        """Make a new stack for a given vm.

        :param name: The name of a virtual machine.

        The options are searched in following files each one providing a
        ``name`` specific section and defaults in the no-name section.

        The directory local file:
        * the ``name`` section in ./uci-vms.conf,
        * the no-name section in ./uci-vms.conf
        The user file:
        * the ``name`` section in ~/uci-vms.conf,
        * the no-name section in ~/uci-vms.conf
        The system-wide file:
        * the ``name`` section in /etc/uci-vms.conf,
        * the no-name section in /etc/uci-vms.conf
        """
        lpath = os.path.abspath('uci-vms.conf')
        self.local_store = self.get_shared_store(VmStore(lpath))
        upath = os.path.join(os.environ['HOME'], 'uci-vms.conf')
        user_store = self.get_shared_store(VmStore(upath))
        spath = os.path.join(system_config_dir(), 'uci-vms.conf')
        self.system_store = self.get_shared_store(VmStore(spath))
        super(VmStack, self).__init__(
            [VmMatcher(self.local_store, name).get_sections,
             VmMatcher(user_store, name).get_sections,
             VmMatcher(self.system_store, name).get_sections,
             ],
            user_store, mutable_section_id=name)


def path_from_unicode(path_string):
    if not isinstance(path_string, unicode):
        raise TypeError
    return os.path.expanduser(path_string)


class PathOption(options.Option):

    def __init__(self, *args, **kwargs):
        """A path option definition.

        This possibly expands the user home directory.
        """
        super(PathOption, self).__init__(
            *args, from_unicode=path_from_unicode, **kwargs)


def register(option):
    options.option_registry.register(option)

register(options.Option('vm', default=None,
                        help_string='''\
The name space defining a virtual machine.

This option is a place holder to document the options that defines a virtual
machine and the options defining the infrastructure used to manage them all.

For qemu based vms, the definition of a vm is stored in an xml file under
'/etc/libvirt/qemu/{vm.name}.xml'. This is under the libvirt package control
and is out of scope for uci-vms.

There are 3 other significant files used for a given vm:

- a disk image mounted at '/' from '/dev/sda1':
  '{vm.images_dir}/{vm.name}.qcow2'

- a iso image available from '/dev/sdb' labeled 'cidata':
  {vm.images_dir}/{vm.name}.seed which contains the cloud-init data used to
  configure/install/update the vm.

- a console: {vm.images_dir}/{vm.name}.console which can be 'tail -f'ed from
  the host.

The data used to create the seed above are stored in a vm specific
configuration directory for easier debug and reference:
- {vm.config_dir}/user-data
- {vm.config_dir}/meta-data
- {vm.config_dir}/ecdsa
- {vm.config_dir}/ecdsa.pub
'''))

# The directory where we store vm files related to their configuration with
# cloud-init (user-data, meta-data, ssh keys).
register(PathOption('vm.vms_dir', default='~/.config/uci-vms',
                    help_string='''\
Where vm related config files are stored.

This includes user-data and meta-data for cloud-init and ssh server keys.

This directory must exist.

Each vm get a specific directory (automatically created) there based on its
name.
'''))
# The base directories where vms are stored for kvm
register(PathOption('vm.images_dir', default='/var/lib/libvirt/images',
                    help_string='''Where vm disk images are stored.''',))
register(options.Option('vm.qemu_etc_dir', default='/etc/libvirt/qemu',
                        help_string='''\
Where libvirt (qemu) stores the vms config files.'''))

# The base directories where vms are stored for lxc
register(PathOption('vm.lxcs_dir', default='/var/lib/lxc',
                    help_string='''Where lxc definitions are stored.'''))
# Isos and images download handling
register(options.Option('vm.iso_url',
                        default='''\
http://cdimage.ubuntu.com/daily-live/current/''',
                        help_string='''Where an iso can be downloaded from.'''
                        ))
register(options.Option('vm.iso_name',
                        default='{vm.release}-desktop-{vm.cpu_model}.iso',
                        help_string='''The name of the iso.'''))
register(options.Option('vm.cloud_image_url',
                        default='''\
http://cloud-images.ubuntu.com/{vm.release}/current/''',
                        help_string='''\
Where a cloud image can be downloaded from.'''))
register(options.Option('vm.cloud_image_name',
                        default='''\
{vm.release}-server-cloudimg-{vm.cpu_model}-disk1.img''',
                        help_string='''The name of the cloud image.'''))
register(PathOption('vm.download_cache', default='{vm.images_dir}',
                    help_string='''Where downloads end up.'''))


# The VM classes are registered where/when needed
vm_class_registry = registries.Registry()


register(options.RegistryOption('vm.class', registry=vm_class_registry,
                                default=options.MANDATORY,
                                help_string='''\
The virtual machine technology to use.'''))
# The ubiquitous vm name
register(options.Option('vm.name', default=None, invalid='error',
                        help_string='''\
The vm name, used as a prefix for related files.'''))
# The second most important bit to define a vm: which ubuntu release ?
register(options.Option('vm.release', default=None, invalid='error',
                        help_string='''The ubuntu release name.'''))
# The third important piece to define a vm: where to store files like the
# console, the user-data and meta-data files, the ssh server keys, etc.
register(options.Option('vm.config_dir', default='{vm.vms_dir}/{vm.name}',
                        invalid='error',
                        help_string='''\
The directory where files specific to a vm are stored.

This includes the user-data and meta-data files used at install time (for
reference and easier debug) as well as the optional ssh server keys.

By default this is {vm.vms_dir}/{vm.name}. You can put it somewhere else by
redefining it as long as it ends up being unique for the vm.

{vm.vms_dir}/{vm.release}/{vm.name} may better suit your taste for example.
'''))
# The options defining the vm physical characteristics
register(options.Option('vm.ram_size', default='1024',
                        help_string='''The ram size in megabytes.'''))
register(options.Option('vm.disk_size', default='8G',
                        help_string='''The disk image size in bytes.

Optional suffixes "k" or "K" (kilobyte, 1024) "M" (megabyte, 1024k) "G"
(gigabyte, 1024M) and T (terabyte, 1024G) are supported.
'''))
register(options.Option('vm.cpus', default='1', help_string='''\
The number of cpus.'''))
register(options.Option('vm.cpu_model', default=None, invalid='error',
                        help_string='''The number of cpus.'''))
register(options.Option('vm.network', default='network=default',
                        invalid='error', help_string='''\
The --network parameter for virt-install.

This can be specialized for each machine but the default should work in most
setups. Watch for your DHCP server exhausting its address space if you create a
lot of vms with random MAC addresses.
'''))

register(options.Option('vm.meta_data', default='''\
instance-id: {vm.name}
local-hostname: {vm.name}
''',
                        invalid='error',
                        help_string='''\
The meta data for cloud-init to put in the seed.'''))

# Some bits that may added to user-data but are optional

register(options.ListOption('vm.packages', default=None,
                            help_string='''\
A list of package names to be installed.'''))
register(options.Option('vm.apt_proxy', default=None, invalid='error',
                        help_string='''\
A local proxy for apt to avoid repeated .deb downloads.

Example:

  vm.apt_proxy = http://192.168.0.42:8000
'''))
register(options.ListOption('vm.apt_sources', default=None,
                            help_string='''\
A list of apt sources entries to be added to the default ones.

Cloud-init already setup /etc/apt/sources.list with appropriate entries. Only
additional entries need to be specified here.
'''))
register(options.ListOption('vm.ssh_authorized_keys', default=None,
                            help_string='''\
A list of paths to public ssh keys to be authorized for the default user.'''))
register(options.ListOption('vm.ssh_keys', default=None,
                            help_string='''A list of paths to server ssh keys.

Both public and private keys can be provided. Accepted ssh key types are rsa,
dsa and ecdsa. The file names should match <type>.*[.pub].
'''))
register(options.Option('vm.update', default=False,
                        from_unicode=options.bool_from_store,
                        help_string='''Whether or not the vm should be updated.

Both apt-get update and apt-get upgrade are called if this option is set.
'''))
register(options.Option('vm.poweroff', default=True,
                        from_unicode=options.bool_from_store,
                        help_string='''\
Whether or not the vm should stop at the end of the installation.'''))
register(options.Option('vm.password', default='ubuntu', invalid='error',
                        help_string='''The ubuntu user password.'''))
register(options.Option('vm.launchpad_id',
                        help_string='''\
The launchpad login used for launchpad ssh access from the guest.'''))
# The scripts that are executed before powering off
register(PathOption('vm.root_script', default=None,
                    help_string='''\
The path to a script executed as root before powering off.

This script is executed before {vm.ubuntu_script}.
'''))
register(PathOption('vm.ubuntu_script', default=None,
                    help_string='''\
The path to a script executed as ubuntu before powering off.

This script is excuted after {vm.root_script}.
'''))
register(options.ListOption('vm.uploaded_scripts', default=None,
                            help_string='''\
A list of scripts to be uploaded to the guest.

Scripts can use config options from their vm, they will be expanded before
upload. All scripts are uploaded into {vm.uploaded_scripts.guest_dir} under
their base name.
'''))
register(options.Option('vm.uploaded_scripts.guest_dir',
                        default='~ubuntu/bin',
                        help_string='''\
Where {vm.uploaded_scripts} are uploaded on the guest.'''))
