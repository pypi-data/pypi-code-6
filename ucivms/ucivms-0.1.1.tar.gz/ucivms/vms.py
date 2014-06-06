#!/usr/bin/env python
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
"""Setup a virtual machine from a config file.

Note: Most of the operations requires root access and this script uses ``sudo``
to get them.
"""
from __future__ import unicode_literals


from cStringIO import StringIO
import errno
import os
import urlparse


import yaml

from ucivms import (
    errors,
    logs,
    monitors,
    ssh,
    subprocesses,
)


class CIUserData(object):
    """Maps configuration data into cloud-init user-data.

    This is a container for the data that will ultimately be encoded into a
    cloud-config-archive user-data file.
    """

    def __init__(self, conf):
        super(CIUserData, self).__init__()
        self.conf = conf
        # The objects we will populate before creating a yaml encoding as a
        # cloud-config-archive file
        self.cloud_config = {}
        self.root_hook = None
        self.ubuntu_hook = None
        self.launchpad_hook = None
        self.uploaded_scripts_hook = None

    def set(self, ud_name, conf_name=None, value=None):
        """Set a user-data option from its corresponding configuration one.

        :param ud_name: user-data key.

        :param conf_name: configuration key, If set to None, `value` should be
            provided.

        :param value: value to use if `conf_name` is None.
        """
        if value is None and conf_name is not None:
            value = self.conf.get(conf_name)
        if value is not None:
            self.cloud_config[ud_name] = value

    def _file_content(self, path, option_name):
        full_path = os.path.expanduser(path)
        try:
            with open(full_path) as f:
                content = f.read()
        except IOError, e:
            if e.args[0] == errno.ENOENT:
                raise errors.ConfigPathNotFound(path, option_name)
            else:
                raise
        return content

    def set_list_of_paths(self, ud_name, conf_name):
        """Set a user-data option from its corresponding configuration one.

        The configuration option is a list of paths and the user-data option
        will be a list of each file content.

        :param ud_name: user-data key.

        :param conf_name: configuration key.
        """
        paths = self.conf.get(conf_name)
        if paths:
            contents = []
            for p in paths:
                contents.append(self._file_content(p, conf_name))
            self.set(ud_name, None, contents)

    def _key_from_path(self, path, option_name):
        """Infer user-data key from file name."""
        ssh_type, kind = ssh.infos_from_path(path)
        if ssh_type is None:
            raise errors.ConfigValueError(option_name, path)
        return '%s_%s' % (ssh_type, kind)

    def set_ssh_keys(self):
        """Set the server ssh keys from a list of paths.

        Provided paths should respect some coding:

        - the base name should start with the ssh type of their key (rsa, dsa,
          ecdsa),

        - base names ending with '.pub' are for public keys, the others are for
          private keys.
        """
        key_paths = self.conf.get('vm.ssh_keys')
        if key_paths:
            ssh_keys = {}
            for p in key_paths:
                key = self._key_from_path(p, 'vm.ssh_keys')
                ssh_keys[key] = self._file_content(p, 'vm.ssh_keys')
            self.set('ssh_keys', None, ssh_keys)

    def set_apt_sources(self):
        sources = self.conf.get('vm.apt_sources')
        if sources:
            apt_sources = []
            for src in sources:
                # '|' should not appear in urls nor keys so it should be safe
                # to use it as a separator.
                parts = src.split('|')
                if len(parts) == 1:
                    apt_sources.append({'source': parts[0]})
                else:
                    # For PPAs, an additional GPG key should be imported in the
                    # guest.
                    apt_sources.append({'source': parts[0], 'keyid': parts[1]})
            self.cloud_config['apt_sources'] = apt_sources

    def append_cmd(self, cmd):
        cmds = self.cloud_config.get('runcmd', [])
        cmds.append(cmd)
        self.cloud_config['runcmd'] = cmds

    def _hook_script_path(self, user):
        return '~%s/uci-vms_post_install' % (user,)

    def _hook_content(self, option_name, user, hook_path, mode='0700'):
        # FIXME: Add more tests towards properly creating a tree on the guest
        # from a tree on the host. There seems to be three kind of items worth
        # caring about here: file content (output path, owner, chmod), file
        # (input and output paths, owner, chmod) and directory (path, owner,
        # chmod). There are also some subtle traps involved about when files
        # are created across various vm generations (one vm creates a dir, a mv
        # on top of that one doesn't, but still creates a file in this dir,
        # without realizing it can fail in a fresh vm). -- vila 2013-03-10
        host_path = self.conf.get(option_name)
        if host_path is None:
            return None
        fcontent = self._file_content(host_path, option_name)
        # Expand options in the provided content so we report better errors
        expanded_content = self.conf.expand_options(fcontent)
        # The following will generate an additional newline at the end of the
        # script. I can't think of a case where it matters and it makes this
        # code more robust (and/or simpler) if the script/file *doesn't* end up
        # with a proper newline.
        # FIXME: This may be worth fixing if we provide a more generic way to
        # create a remote tree. -- vila 2013-03-10
        hook_content = '''#!/bin/sh
cat >{__guest_path} <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
{__fcontent}
EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown {__user}:{__user} {__guest_path}
chmod {__mode} {__guest_path}
'''
        return hook_content.format(__user=user, __fcontent=expanded_content,
                                   __mode=mode,
                                   __guest_path=hook_path)

    def set_boot_hook(self):
        # FIXME: Needs a test ensuring we execute as root -- vila 2013-03-07
        hook_path = self._hook_script_path('root')
        content = self._hook_content('vm.root_script', 'root', hook_path)
        if content is not None:
            self.root_hook = content
            self.append_cmd(hook_path)

    def set_ubuntu_hook(self):
        # FIXME: Needs a test ensuring we execute as ubuntu -- vila 2013-03-07
        hook_path = self._hook_script_path('ubuntu')
        content = self._hook_content('vm.ubuntu_script', 'ubuntu', hook_path)
        if content is not None:
            self.ubuntu_hook = content
            self.append_cmd(['su', '-l', '-c', hook_path, 'ubuntu'])

    def set_launchpad_access(self):
        # FIXME: Needs a test that we can really access launchpad properly via
        # ssh. Can only be done as a real launchpad user and as such requires
        # cooperation :) I.e. Some configuration option set by the user will
        # trigger the test -- vila 2013-03-14
        lp_id = self.conf.get('vm.launchpad_id')
        if lp_id is None:
            return
        # FIXME: There is no config option to define the key name
        # (<lp_id>@uci-vms) -- vila 2014-01-16
        # Use the specified ssh key found in ~/.ssh as the private key. The
        # user is supposed to have uploaded the public one.
        local_path = os.path.join('~', '.ssh', '%s@uci-vms' % (lp_id,))
        # Force id_rsa or we'll need a .ssh/config to point to user@uci-vms
        # for .lauchpad.net.
        hook_path = '/home/ubuntu/.ssh/id_rsa'
        dir_path = os.path.dirname(hook_path)
        try:
            fcontent = self._file_content(local_path, 'vm.launchpad_id')
        except errors.ConfigPathNotFound, e:
            # Override the fmt for this specific exception to give a better
            # explanation.
            e.fmt = ('You need to create the {p} keypair and upload {p}.pub to'
                     ' launchpad.\n'
                     'See vm.launchpad_id in README.'.format(p=local_path))
            raise e
        # FIXME: ~Duplicated from _hook_content. -- vila 2013-03-10

        # FIXME: If this hook is executed before the ubuntu user is created we
        # need to chown/chmod ~ubuntu which is bad. This happens when a
        # -pristine vm is created and lead to GUI login failing because it
        # can't create any dir/file there. The fix is to only create a script
        # that will be executed via runcmd so it will run later and avoid the
        # issue. -- vila 2013-03-21
        # FIXME: Moreover, -pristine vms don't have bzr installed so this
        # cannot succeed there -- vila 2013-08-07
        hook_content = '''#!/bin/sh
mkdir -p {dir_path}
chown {user}:{user} ~ubuntu
chmod {dir_mode} ~ubuntu
chown {user}:{user} {dir_path}
chmod {dir_mode} {dir_path}
cat >{guest_path} <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
{fcontent}
EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown {user}:{user} {guest_path}
chmod {file_mode} {guest_path}
'''
        self.launchpad_hook = self.conf.expand_options(
            hook_content,
            env=dict(user='ubuntu', fcontent=fcontent,
                     file_mode='0400', guest_path=hook_path,
                     dir_mode='0700', dir_path=dir_path))
        self.append_cmd(['sudo', '-u', 'ubuntu',
                         'bzr', 'launchpad-login', lp_id])

    def set_uploaded_scripts(self):
        script_paths = self.conf.get('vm.uploaded_scripts')
        if not script_paths:
            return
        hook_path = '~ubuntu/uci-vms_uploads'
        bindir = self.conf.get('vm.uploaded_scripts.guest_dir')
        out = StringIO()
        out.write('''#!/bin/sh
cat >{hook_path} <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
mkdir -p {bindir}
cd {bindir}
'''.format(**locals()))
        for path in script_paths:
            fcontent = self._file_content(path, 'vm.uploaded_scripts')
            expanded = self.conf.expand_options(fcontent)
            base = os.path.basename(path)
            # FIXME: ~Duplicated from _hook_content. -- vila 2012-03-15
            out.write('''cat >{base} <<'EOF{base}'
{expanded}
EOF{base}
chmod 0755 {base}
'''.format(**locals()))

        out.write('''EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown {user}:{user} {hook_path}
chmod 0700 {hook_path}
'''.format(user='ubuntu', **locals()))
        self.uploaded_scripts_hook = out.getvalue()
        self.append_cmd(['su', '-l', '-c', hook_path, 'ubuntu'])

    def set_poweroff(self):
        # We want to shutdown properly after installing. This is safe to set
        # here as subsequent boots will ignore this setting, letting us use the
        # vm ;)
        if self.conf.get('vm.poweroff'):
            if self.conf.get('vm.release') in ('precise', 'quantal'):
                # Curse cloud-init lack of compatibility
                self.append_cmd('halt')
            else:
                self.set('power_state', None, {'mode': 'poweroff'})

    def populate(self):
        # Common and non-configurable options
        self.set('manage_etc_hosts', None, True)
        self.set('chpasswd', None, dict(expire=False))
        # Configurable options
        if self.conf.get('vm.release') == 'precise':
            # Curse cloud-init lack of compatibility
            msg = 'uci-vms finished installing in $UPTIME seconds.'
        else:
            msg = 'uci-vms finished installing in ${uptime} seconds.'
        self.set('final_message', None, msg)
        self.set('password', 'vm.password')
        self.set_list_of_paths('ssh_authorized_keys', 'vm.ssh_authorized_keys')
        self.set_ssh_keys()
        self.set('apt_proxy', 'vm.apt_proxy')
        # Both user-data keys are set from the same config key, we don't
        # provide a finer access.
        self.set('apt_update', 'vm.update')
        self.set('apt_upgrade', 'vm.update')
        self.set_apt_sources()
        self.set('packages', 'vm.packages')
        self.set_launchpad_access()
        # uploaded scripts
        self.set_uploaded_scripts()
        # The commands executed before powering off
        self.set_boot_hook()
        self.set_ubuntu_hook()
        # This must be called last so previous commands (for precise and
        # quantal) can be executed before powering off
        self.set_poweroff()

    def add_boot_hook(self, parts, hook):
        if hook is not None:
            parts.append({'content': '#cloud-boothook\n' + hook})

    def dump(self):
        parts = [{'content': '#cloud-config\n'
                  + yaml.safe_dump(self.cloud_config)}]
        self.add_boot_hook(parts, self.root_hook)
        self.add_boot_hook(parts, self.ubuntu_hook)
        self.add_boot_hook(parts, self.launchpad_hook)
        self.add_boot_hook(parts, self.uploaded_scripts_hook)
        # Wrap the lot into a cloud config archive
        return '#cloud-config-archive\n' + yaml.safe_dump(parts)


class VM(object):
    """A virtual machine relying on cloud-init to customize installation."""

    def __init__(self, conf):
        self.conf = conf
        # Seed files
        self._meta_data_path = None
        self._user_data_path = None
        self.ci_user_data = None

    def _download_in_cache(self, source_url, name, force=False):
        """Download ``name`` from ``source_url`` in ``vm.download_cache``.

        :param source_url: The url where the file to download is located

        :param name: The name of the file to download (also used as the name
            for the downloaded file).

        :param force: Remove the file from the cache if present.

        :return: False if the file is in the download cache, True if a download
            occurred.
        """
        source = urlparse.urljoin(source_url, name)
        download_dir = self.conf.get('vm.download_cache')
        if not os.path.exists(download_dir):
            raise errors.ConfigValueError('vm.download_cache', download_dir)
        target = os.path.join(download_dir, name)
        # FIXME: By default the download dir may be under root control, but if
        # a user chose to use a different one under his own control, it would
        # be nice to not require sudo usage. -- vila 2013-02-06
        if force:
            subprocesses.run(['sudo', 'rm', '-f', target])
        if not os.path.exists(target):
            # FIXME: We do ask for a progress bar but it's not displayed
            # (subprocesses.run capture both stdout and stderr) ! At least
            # while used interactively, it should. -- vila 2013-02-06
            subprocesses.run(['sudo', 'wget', '--progress=dot:mega', '-O',
                              target, source])
            return True
        else:
            return False

    def ensure_dir(self, path):
        try:
            os.mkdir(path)
        except OSError, e:
            # FIXME: Try to create the parent dir ?
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

    def config_dir_path(self):
        # FIXME: expanduser is not tested
        return os.path.expanduser(self.conf.get('vm.config_dir'))

    def console_path(self):
        # The console is used to record 'setup' and 'start' outputs
        return os.path.join(self.config_dir_path(), 'console')

    # MISSINGTEST -- vila 2014-01-18
    def empty_console(self):
        # The console file is created during setup. As such it's created by
        # root. Care should be taken to ensure the file receives proper chmod
        # bits (or only root will be able to read it) and that it's reset at
        # the right time ('setup' is a good time as it means the console will
        # contain the creation of the instance and all its 'start' uses).
        self.ensure_dir(self.config_dir_path())
        # Create/empty the file so we get access to it (otherwise it will be
        # owned by root).
        open(self.console_path(), 'w').close()

    def ssh_keygen(self, force=False):
        self.ensure_dir(self.config_dir_path())
        keys = self.conf.get('vm.ssh_keys')
        for key in keys:
            if force or not os.path.exists(key):
                ssh.keygen(key, self.conf.get('vm.name'))

    def create_meta_data(self):
        self.ensure_dir(self.config_dir_path())
        self._meta_data_path = os.path.join(self.config_dir_path(),
                                            'meta-data')
        with open(self._meta_data_path, 'w') as f:
            f.write(self.conf.get('vm.meta_data'))

    def create_user_data(self):
        ci_user_data = CIUserData(self.conf)
        ci_user_data.populate()
        self.ensure_dir(self.config_dir_path())
        self._user_data_path = os.path.join(self.config_dir_path(),
                                            'user-data')
        with open(self._user_data_path, 'w') as f:
            f.write(ci_user_data.dump())
        self.ci_user_data = ci_user_data

    def download(self, force=False):
        raise NotImplementedError(self.download)

    def iface_path(self, iface):
        return os.path.join(self.config_dir_path(),
                            'interface.{}'.format(iface))

    def capture_interface(self, line, iface_re):
        """Capture the required interface if it appears in 'line'.

        :param line: A line from the vm console.

        :param iface_re: The regexp matching a cloud-init output revealing an
            interface.

        :return: True if the interface was captured, False otherwise.
        """
        match = iface_re.match(line)
        if match is not None:
            ip, mask, mac = match.groups()
            with open(self.iface_path(iface_re.iface), 'w') as f:
                f.write(' '.join((ip, mask, mac)) + '\n')
                return True
        return False

    def get_interface(self, iface):
        try:
            with open(self.iface_path(iface)) as f:
                content = f.read()
                ip, mask, mac = content.split()
                return ip, mask, mac
        except OSError as e:
            if e.errno == errno.ENOENT:
                # Unknown interface
                return None
            else:
                raise

    def scan_console_during_install(self, console_size, cmd):
        """Scan the console output until the end of the install.

        We added a specific part for cloud-init to ensure we properly detect
        the end of the run.

        :param console_size: The size of the console file before 'install' is
            run.

        :param cmd: The install command (used for error display).
        """
        console = monitors.TailMonitor(self.console_path(), console_size)
        iface = 'eth0'
        iface_re = logs.InterfaceRegexp(iface)
        try:
            for line in console.scan():
                # FIXME: We need some way to activate this dynamically (conf
                # var defaulting to environment variable OR cmdline parameter ?
                # -- vila 2013-02-11

#                print "read: [%s]" % (line,) # so useful for debug...
                self.capture_interface(line, iface_re)
                # FIXME: This bare 'pass' smells. Something is wrong in the
                # design. -- vila 2014-01-18
                pass
        except (errors.ConsoleEOFError, errors.CloudInitError):
            # FIXME: No test covers this path -- vila 2013-02-15
            err_lines = ['Suspicious line from cloud-init.\n',
                         '\t' + console.lines[-1],
                         'Check the configuration:\n']
            with open(self._meta_data_path) as f:
                err_lines.append('meta-data content:\n')
                err_lines.extend(f.readlines())
            with open(self._user_data_path) as f:
                err_lines.append('user-data content:\n')
                err_lines.extend(f.readlines())
            raise errors.CommandError(cmd, console.proc.returncode,
                                      '\n'.join(console.lines),
                                      ''.join(err_lines))

    # MISSINGTEST -- vila 2014-01-18
    def scan_console_during_start(self, console_size, cmd):
        """Scan the console output while the instance starts.

        This is used to capture the network addresses displayed by cloud-init.

        :param console_size: The size of the console file before 'start' is
            run.

        :param cmd: The start command (used for error display).
        """
        console = monitors.TailMonitor(self.console_path(), console_size)
        iface = 'eth0'
        iface_re = logs.InterfaceRegexp(iface)
        try:
            for line in console.scan():
                if self.capture_interface(line, iface_re):
                    # We're done, no need to scan anymore (and work around the
                    # fact that 'scan' will otherwise terminate when the vm is
                    # stopped ;)
                    return
        except errors.ConsoleEOFError:
            # We're done
            pass

    def shell(self, command, *args):
        iface = 'eth0'
        ip, _, _ = self.get_interface(iface)
        proc = subprocesses.ssh('ubuntu', ip, command, *args)
        return proc.returncode


def kvm_states(source=None):
    """A dict of states for kvms indexed by name.

    :param source: A list of lines as produced by virsh list --all without
        decorations (header/footer).
    """
    if source is None:
        retcode, out, err = subprocesses.run(['virsh', 'list', '--all'])
        # Get rid of header/footer
        source = out.splitlines()[2:-1]
    states = {}
    for line in source:
        caret_or_id, name, state = line.split(None, 2)
        states[name] = state
    return states


class Kvm(VM):

    def __init__(self, conf):
        super(Kvm, self).__init__(conf)
        # Disk paths
        self._disk_image_path = None
        self._seed_path = None

    def state(self):
        states = kvm_states()
        try:
            state = states[self.conf.get('vm.name')]
        except KeyError:
            state = None
        return state

    def download_iso(self, force=False):
        """Download the iso to install the vm.

        :return: False if the iso is in the download cache, True if a download
            occurred.
        """
        return self._download_in_cache(self.conf.get('vm.iso_url'),
                                       self.conf.get('vm.iso_name'),
                                       force=force)

    def download_cloud_image(self, force=False):
        """Download the cloud image to install the vm.

        :return: False if the image is in the download cache, True if a
            download occurred.
        """
        return self._download_in_cache(self.conf.get('vm.cloud_image_url'),
                                       self.conf.get('vm.cloud_image_name'),
                                       force=force)

    def download(self, force=False):
        return self.download_cloud_image(force)

    def create_seed_image(self):
        if self._meta_data_path is None:
            self.create_meta_data()
        if self._user_data_path is None:
            self.create_user_data()
        images_dir = self.conf.get('vm.images_dir')
        seed_path = os.path.join(
            images_dir, self.conf.expand_options('{vm.name}.seed'))
        subprocesses.run(
            # We create the seed in the ``vm.images_dir`` directory, so
            # ``sudo`` is required
            ['sudo',
             'genisoimage', '-output', seed_path,
             # cloud-init relies on the volid to discover its data
             '-volid', 'cidata',
             '-joliet', '-rock', '-input-charset', 'default',
             '-graft-points',
             'user-data=%s' % (self._user_data_path,),
             'meta-data=%s' % (self._meta_data_path,),
             ])
        self._seed_path = seed_path

    def create_disk_image(self):
        if self.conf.get('vm.backing') is None:
            self.create_disk_image_from_cloud_image()
        else:
            self.create_disk_image_from_backing()

    def create_disk_image_from_cloud_image(self):
        """Create a disk image from a cloud one."""
        cloud_image_path = os.path.join(
            self.conf.get('vm.download_cache'),
            self.conf.get('vm.cloud_image_name'))
        disk_image_path = os.path.join(
            self.conf.get('vm.images_dir'),
            self.conf.expand_options('{vm.name}.qcow2'))
        subprocesses.run(
            ['sudo', 'qemu-img', 'convert',
             '-O', 'qcow2', cloud_image_path, disk_image_path])
        subprocesses.run(
            ['sudo', 'qemu-img', 'resize',
             disk_image_path, self.conf.get('vm.disk_size')])
        self._disk_image_path = disk_image_path

    def create_disk_image_from_backing(self):
        """Create a disk image backed by an existing one."""
        backing_image_path = os.path.join(
            self.conf.get('vm.images_dir'),
            self.conf.expand_options('{vm.backing}'))
        disk_image_path = os.path.join(
            self.conf.get('vm.images_dir'),
            self.conf.expand_options('{vm.name}.qcow2'))
        subprocesses.run(
            ['sudo', 'qemu-img', 'create', '-f', 'qcow2',
             '-b', backing_image_path, disk_image_path])
        subprocesses.run(
            ['sudo', 'qemu-img', 'resize',
             disk_image_path, self.conf.get('vm.disk_size')])
        self._disk_image_path = disk_image_path

    def scan_console_during_install(self, console_size, cmd):
        """See Vm.scan_console_during_install."""
        # The console is re-created by virt-install (even if we created it
        # before) which requires sudo but creates the file 0600 for
        # libvirt-qemu. We give read access to all otherwise 'tail -f' requires
        # sudo and can't be killed anymore.
        subprocesses.run(['sudo', 'chmod', '0644', self.console_path()])
        # While `virt-install` is running, let's connect to the console
        super(Kvm, self).scan_console_during_install(console_size, cmd)

    def install(self):
        # Create a kvm, relying on cloud-init to customize the base image.
        #
        # There are two processes involvded here:
        # - virt-install creates the vm and boots it.
        # - progress is monitored via the console to detect cloud-final.
        #
        # Once cloud-init has finished, the vm can be powered off.

        # FIXME: If the install doesn't finish after $time, emit a warning and
        # terminate self.install_proc.
        # FIXME: If we can't connect to the console, emit a warning and
        # terminate console and self.install_proc.
        # FIXME: If we don't receive anything on the console after $time2, emit
        # a warning and terminate console and self.install_proc.
        # -- vila 2013-02-07
        if self._seed_path is None:
            self.create_seed_image()
        if self._disk_image_path is None:
            self.create_disk_image()
        self.empty_console()
        virt_install = [
            'sudo', 'virt-install',
            # To ensure we're not bitten again by http://pad.lv/1157272 where
            # virt-install wrongly detect virtualbox. -- vila 2013-03-20
            '--connect', 'qemu:///system',
            # Without --noautoconsole, virt-install will relay the console,
            # that's not appropriate for our needs so we'll connect later
            # ourselves
            '--noautoconsole',
            # We define the console as a file so we can monitor the install
            # via 'tail -f'
            '--serial', 'file,path={}'.format(self.console_path()),
            '--network', self.conf.get('vm.network'),
            # Anticipate that we'll need a graphic card defined
            '--graphics', 'spice',
            '--name', self.conf.get('vm.name'),
            '--ram', self.conf.get('vm.ram_size'),
            '--vcpus', self.conf.get('vm.cpus'),
            '--disk', 'path=%s,format=qcow2' % (self._disk_image_path,),
            '--disk', 'path=%s' % (self._seed_path,),
            # We just boot, cloud-init will handle the installs we need
            '--boot', 'hd', '--hvm',
        ]
        console_size = monitors.actual_file_size(self.console_path())
        subprocesses.run(virt_install)
        self.scan_console_during_install(console_size, virt_install)
        # We've seen the console signaling halt, but the vm will need a bit
        # more time to get there so we help it a bit.
        if self.conf.get('vm.release') in ('precise', 'quantal'):
            # cloud-init doesn't implement power_state until raring and need a
            # gentle nudge.
            self.poweroff()
        while True:
            state = self.state()
            # We expect the vm's state to be 'in shutdown' but in some rare
            # occasions we may catch 'running' before getting 'in shutdown'.
            if state in ('in shutdown', 'running'):
                # Ok, querying the state takes time, this regulates the polling
                # enough that we don't need to sleep.
                continue
            elif state == 'shut off':
                # Good, we're done
                break
            # FIXME: No idea on how to test the following. Manually tested by
            # altering the expected state above and running 'selftest.py -v'
            # which errors out for test_install_with_seed and
            # test_install_backing. Also reproduced when 'running' wasn't
            # expected before 'in shutdown' -- vila 2013-02-19
            # Unexpected state reached, bad.
            raise errors.UciVmsError(
                'Something went wrong during {name} install\n'
                'The vm ended in state: {state}\n'
                'Check the console at {path}',
                name=self.conf.get('vm.name'), state=state,
                path=self.console_path())

    def start(self):
        start_cmd = ['sudo', 'virsh', 'start', self.conf.get('vm.name')]
        console_size = monitors.actual_file_size(self.console_path())
        if console_size is None:
            # FIXME: This is needed because the following can fail (real life):
            # 'rm -f ~/vms/kvm1/console ; ./uci-vms start kvm1' because
            # virst start creates the console file as root if it doesn't exist
            self.empty_console()
            console_size = 0
        proc = subprocesses.run(start_cmd)
        self.scan_console_during_start(console_size, start_cmd)
        return proc

    def poweroff(self):
        return subprocesses.run(
            ['sudo', 'virsh', 'destroy', self.conf.get('vm.name')])

    def undefine(self):
        return subprocesses.run(
            ['sudo', 'virsh', 'undefine', self.conf.get('vm.name'),
             '--remove-all-storage'])


def lxc_info(vm_name, source=None):
    """Scan state info from the lxc-info output.

    :param vm_name: The vm we want to query about.

    :param source: A list of lines as produced by lxc-info -n vm.name.
    """
    if source is None:
        retcode, out, err = subprocesses.run(
            ['sudo', 'lxc-info', '-n', vm_name])
        source = out.splitlines()
    state_line = source[0]
    if len(source) > 1:
        pid_line = source[1]
    else:
        # Recent lxc versions stopped outputting the fake pid, let's do that
        # ourselves -- vila 2013-10-09
        pid_line = 'pid: -1'
    _, state = state_line.split(None, 1)
    _, pid = pid_line.split(None, 1)
    return dict(state=state, pid=pid)


class Lxc(VM):

    def __init__(self, conf):
        super(Lxc, self).__init__(conf)
        self._guest_seed_path = None
        self._fstab_path = None

    def state(self):
        info = lxc_info(self.conf.get('vm.name'))
        return info['state']

    def download(self, force=False):
        # FIXME: lxc-create provides its own cache. download(True) should just
        # ensure we clear that cache from the previous download. Should we add
        # a warning ?  Specialize the cache for Kvm only ?-- vila 2013-08-07
        return True

    def create_seed_files(self):
        if self._meta_data_path is None:
            self.create_meta_data()
        if self._user_data_path is None:
            self.create_user_data()
        self._fstab_path = os.path.join(self.config_dir_path(), 'fstab')
        self._guest_seed_path = os.path.join(
            self.conf.get('vm.lxcs_dir'),
            self.conf.get('vm.name'),
            'rootfs/var/lib/cloud/seed/nocloud-net')
        with open(self._fstab_path, 'w') as f:
            # Add a entry so cloud-init find the seed files
            f.write('%s %s none bind 0 0\n' % (self.config_dir_path(),
                                               self._guest_seed_path))

    def install(self):
        '''Create an lxc, relying on cloud-init to customize the base image.

        There are two processes involvded here:
        - lxc-create creates the vm.
        - progress is monitored via the console to detect cloud-final.

        Once cloud-init has finished, the vm can be powered off.
        '''
        # FIXME: use python3-lxc ?

        # FIXME: If the install doesn't finish after $time, emit a warning and
        # terminate self.install_proc.
        # FIXME: If we can't connect to the console, emit a warning and
        # terminate console and self.install_proc.
        # FIXME: If we don't receive anything on the console after $time2, emit
        # a warning and terminate console and self.install_proc.
        # -- vila 2013-02-07
        if self._fstab_path is None:
            self.create_seed_files()
        self.empty_console()
        # FIXME: Some feedback would be nice during lxc creation, not sure
        # about which errors to expect there either -- vila 2013-08-07
        lxc_create = ['sudo', 'lxc-create',
                      '-n', self.conf.get('vm.name'),
                      '-t', 'ubuntu-cloud',
                      '--',
                      '-r', self.conf.get('vm.release'),
                      '-a', self.conf.get('vm.cpu_model'),
                      '--userdata', self._user_data_path,
                      '--hostid', self.conf.get('vm.name'),
                      ]
        _, out, err = subprocesses.run(lxc_create)
        # FIXME: useful for debug, needs a config option -- vila 2014-01-17
        # print('lxc-create, \n\tout: {}\n\t{}'.format(out, err))
        # Now we add the cloud-init data seed and do lxc-start to trigger all
        # our customizations monitoring the lxc-start output from the host.
        lxc_start = ['sudo', 'lxc-start',
                     '-n', self.conf.get('vm.name'),
                     '--console-log', self.console_path(),
                     # Daemonize or: 1) it fails with a spurious return code,
                     # 2) We can't monitor the logfile
                     '-d',
                     ]
        # FIXME: useful for debug, needs a config option -- vila 2014-01-17
        # print 'cmd: %s' % (' '.join(lxc_start),)
        console_size = monitors.actual_file_size(self.console_path())
        proc = subprocesses.run(lxc_start)
        self.scan_console_during_install(console_size, lxc_start)
        return proc

    def start(self):
        start_cmd = ['sudo', 'lxc-start', '-n', self.conf.get('vm.name'),
                     '--console-log', self.console_path(),
                     # Starts in daemon mode or we end up with an interactive
                     # session
                     '-d',
                     ]
        console_size = monitors.actual_file_size(self.console_path())
        if console_size is None:
            # FIXME: This is needed because the following can fail (real life):
            # 'rm -f ~/vms/lxc1/console ; ./uci-vms start lxc1' because
            # lxc-start creates the console file as root if it doesn't exist
            self.empty_console()
            console_size = 0
        proc = subprocesses.run(start_cmd)
        self.scan_console_during_start(console_size, start_cmd)
        return proc

    def poweroff(self):
        return subprocesses.run(
            ['sudo', 'lxc-stop', '-n', self.conf.get('vm.name')])

    def undefine(self):
        try:
            return subprocesses.run(
                ['sudo', 'lxc-destroy', '-n', self.conf.get('vm.name')])
        except errors.CommandError as e:
            # FIXME: No test -- vila 2013-08-08
            not_exist = 'does not exist\n'
            not_defined = 'is not defined\n'
            if (e.err.endswith(not_exist) or e.err.endswith(not_defined)):
                # lxc-destroy does not always make a distinction between a
                # stopped vm and a non-existing one.
                pass
            else:
                raise
