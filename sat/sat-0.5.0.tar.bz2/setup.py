#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT: a jabber client
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014  Jérôme Poisson (goffi@goffi.org)
# Copyright (C) 2013, 2014 Adrien Cossa (souliane@mailoo.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ez_setup import use_setuptools
use_setuptools()
from setuptools.command.install import install
from setuptools import setup
from distutils.file_util import copy_file
import os
import os.path
import sys
import subprocess
from stat import ST_MODE
import shutil
import re

# seen here: http://stackoverflow.com/questions/7275295
try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        pkgs = dict.fromkeys(
            [_top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
                if _top_level_package(k) != "twisted"
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names


NAME = 'sat'
LAUNCH_DAEMON_COMMAND = 'sat'

ENV_SAT_INSTALL = "SAT_INSTALL"  # environment variable to customise installation
NO_PREINSTALL_OPT = 'nopreinstall'  # skip all preinstallation checks
AUTO_DEB_OPT = 'autodeb'  # automaticaly install debs
NO_X_OPT = 'nox'  # don't install X dependant packages
CLEAN_OPT = 'clean'  # remove previous installation directories
PURGE_OPT = 'purge'  # remove building and previous installation directories
DBUS_DIR = 'dbus-1/services'
DBUS_FILE = 'misc/org.goffi.SAT.service'

# Following map describe file to adapt with installation path:
# key is the self attribute to get (e.g.: sh_script_path will modify self.sh_script_path file)
# value is a dict where key is the regex of the part to change, and value is either the string
# to replace or a tuple with a template and values to replace (if value to replace is a string,
# the attribute from self with that name will be used).
FILE_ADJ = {'sh_script_path': {r'PYTHON *=.*': 'PYTHON="{}"'.format(sys.executable)},
            'dbus_service_path': {r'Exec *=.*': ('Exec={}', 'sh_script_path_final')},
           }


class MercurialException(Exception):
    pass


def module_installed(module_name):
    """Try to import module_name, and return False if it failed
    @param module_name: name of the module to test
    @return: True if successful"""
    try:
        __import__(module_name)
    except ImportError:
        return False
    return True


class CustomInstall(install):

    def adapt_files(self):
        """Adapt files to installed environments

        Mainly change the paths
        """
        def adapter(ordered_replace, match_obj):
            """do file adjustment, getting self attribute when needed"""
            idx = match_obj.lastindex - 1
            repl_data = ordered_replace[idx][1]
            if isinstance(repl_data, tuple):
                template = repl_data[0]
                args = [getattr(self, arg) if isinstance(arg, basestring) else arg for arg in repl_data[1:]]
                return template.format(*args)
            return repl_data

        for file_attr, replace_data in FILE_ADJ.iteritems():
            file_path = getattr(self, file_attr)
            ordered_replace = [(regex, repl) for regex, repl in replace_data.iteritems()]
            regex = '|'.join(('({})'.format(regex) for regex, dummy in ordered_replace))
            with open(file_path, 'r') as f:
                buff = f.read()
            buff = re.sub(regex, lambda match_obj: adapter(ordered_replace, match_obj), buff)
            with open(file_path, 'w') as f:
                f.write(buff)

    def custom_create_links(self):
        """Create symbolic links to executables"""
        # the script which launch the daemon
        for source, dest in self.sh_script_links:
            if self.root is None:
                if os.path.islink(dest) and os.readlink(dest) != source:
                    os.remove(dest)  # copy_file doesn't force the link update
                dest_name, copied = copy_file(source, dest, link='sym')
                assert copied
                # we change the perm in the same way as in the original install_scripts
                mode = ((os.stat(dest_name)[ST_MODE]) | 0555) & 07777
                os.chmod(dest_name, mode)
            else:
                # if root is not None, source probably doesn't exist yet
                # this is not managed by copy_file, so we must use os.symlink directly
                if os.path.islink(dest):
                    os.remove(dest)  # symlink doesn't force the link update
                os.symlink(source, dest)

    def run(self):
        if not self.root:
            ignore_idx = 0
        else:
            ignore_idx = len(self.root)
            if self.root[-1] == '/':
                ignore_idx-=1 # we dont want to remove the first '/' in _final paths
        # _final suffixed attributes are the ones without the self.root prefix path
        # it's used at least on Arch linux installation as install is made on a local $pkgdir
        # which is later moved to user's FS root
        self.install_lib_final = self.install_lib[ignore_idx:]
        self.sh_script_path = os.path.join(self.install_lib, NAME, 'sat.sh')
        self.sh_script_path_final = os.path.join(self.install_lib_final, NAME, 'sat.sh')
        self.sh_script_links = [(self.sh_script_path_final, os.path.join(self.install_scripts, LAUNCH_DAEMON_COMMAND))]
        self.dbus_service_path = os.path.join(self.install_data, 'share', DBUS_DIR, os.path.basename(DBUS_FILE))
        sys.stdout.write('running pre installation stuff\n')
        sys.stdout.flush()
        if PURGE_OPT in install_opt:
            self.purge()
        elif CLEAN_OPT in install_opt:
            self.clean()
        install.run(self)
        sys.stdout.write('running post installation stuff\n')
        sys.stdout.flush()
        self.adapt_files()
        self.custom_create_links()

    def confirm(self, message):
        """Ask the user for a confirmation"""
        message += 'Proceed'
        while True:
            res = raw_input("%s (y/n)? " % message)
            if res not in ['y', 'Y', 'n', 'N']:
                print "Your response ('%s') was not one of the expected responses: y, n" % res
                message = 'Proceed'
                continue
            if res in ('y', 'Y'):
                return True
            return False

    def clean(self, message=None, to_remove=None):
        """Clean previous installation directories

        @param message (str): to use a non-default confirmation message
        @param to_remove (str): extra files/directories to remove
        """
        if message is None:
            message = "Cleaning previous installation directories"
        if to_remove is None:
            to_remove = []
        for path in [os.path.join(self.install_lib, NAME),
                     os.path.join(self.install_lib, "%s_frontends" % NAME),
                     os.path.join(self.install_data, 'share', 'doc', NAME),
                     os.path.join(self.install_lib, "%s.egg-info" % self.config_vars['dist_fullname']),
                     os.path.join(self.install_lib, "%s-py%s.egg-info" % (self.config_vars['dist_fullname'], self.config_vars['py_version_short'])),
                     ]:
            if os.path.isdir(path):
                to_remove.append(path)
        for source, dest in self.sh_script_links:
            if os.path.islink(dest):
                to_remove.append(dest)

        for script in ('jp', 'wix', 'primitivus'):
            dest = os.path.join(self.install_scripts, script)
            if os.path.exists(dest):
                to_remove.append(dest)

        message = "%s:\n%s\n" % (message, "\n".join(["    %s" % path for path in to_remove]))
        if not self.confirm(message):
            return
        sys.stdout.write('cleaning previous installation directories...\n')
        sys.stdout.flush()
        for path in to_remove:
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)

    def purge(self):
        """Clean building and previous installation directories"""
        message = "Cleaning building and previous installation directories"
        to_remove = [os.path.join(os.getcwd(), 'build')]
        self.clean(message, to_remove)


def preinstall_check(install_opt):
    """Check presence of problematic dependencies, and try to install them with package manager
    This ugly stuff is necessary as distributions are not installed correctly with setuptools/distribute
    Hope to remove this at some point"""

    #modules_tocheck = ['twisted', 'twisted.words', 'twisted.web', 'wx', 'urwid']
    modules_tocheck = ['gobject']  # XXX: python-gobject is not up-to-date in PyPi
    if NO_X_OPT not in install_opt:
        modules_tocheck.append('wx') # wx is the only one to be really difficult to install

    package = {'twisted': 'python-twisted-core',
               'twisted.words': 'python-twisted-words',
               'twisted.web': 'python-twisted-web',
               'wx': 'python-wxgtk2.8',
               'urwid': 'python-urwid',
               'gobject': 'python-gobject',
               'mercurial': 'mercurial'}  # this dict map dependencies to packages names for debian distributions

    sys.stdout.write("Running pre-installation dependencies check\n")

    # which modules are not installed ?
    modules_toinstall = [mod for mod in modules_tocheck if not module_installed(mod)]
    """# is mercurial available ?
    hg_installed = subprocess.call('which hg', stdout=open('/dev/null', 'w'), shell=True) == 0
    if not hg_installed:
        modules_toinstall.append('mercurial')"""  # hg can be installed from pypi

    if modules_toinstall:
        if AUTO_DEB_OPT in install_opt:  # auto debian installation is requested
            # are we on a distribution using apt ?
            apt_path = subprocess.Popen('which apt-get', stdout=subprocess.PIPE, shell=True).communicate()[0][:-1]
        else:
            apt_path = None

        not_installed = set()
        if apt_path:
            # we have apt, we'll try to use it
            for module_name in modules_toinstall:
                package_name = package[module_name]
                sys.stdout.write("Installing %s\n" % package_name)
                success = subprocess.call('%s -qy install %s' % (apt_path, package_name), shell=True) == 0
                if not success:
                    not_installed.add(module_name)
        else:
            not_installed = set(modules_toinstall)

        if not_installed:
            # some packages can't be automatically installed, we print their name for manual installation
            sys.stdout.write("You should install the following dependencies with your distribution recommanded tool before installing %s:\n" % NAME)
            for module_name in not_installed:
                sys.stdout.write("- %s (Debian name: %s)\n" % (module_name, package[module_name]))
            sys.exit(2)


if sys.argv[1].lower() in ['egg_info', 'install']:
    # we only check dependencies if egg_info or install is used
    install_opt = os.environ.get(ENV_SAT_INSTALL, "").split()
    if not NO_PREINSTALL_OPT in install_opt:  # user can force preinstall skipping
        preinstall_check(install_opt)

setup(name=NAME,
      version='0.5.0',
      description=u'Salut à Toi multi-frontend XMPP client',
      long_description=u'Salut à Toi (SàT) is a XMPP client based on a daemon/frontend architecture. Its multi-frontends (desktop, web, console interface, CLI, etc) and multi-purposes (instant messaging, microblogging, games, file sharing, etc).',
      author='Association « Salut à Toi »',
      author_email='contact@goffi.org',
      url='http://salut-a-toi.org',
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Environment :: X11 Applications :: GTK',
                   'Framework :: Twisted',
                   'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                   'Operating System :: POSIX :: Linux',
                   'Topic :: Communications :: Chat'],
      package_dir={'sat': 'src', 'sat_frontends': 'frontends/src', 'twisted.plugins': 'src/twisted/plugins'},
      packages=['sat', 'sat.tools', 'sat.bridge', 'sat.plugins', 'sat.test', 'sat.core', 'sat.memory',
                'sat_frontends', 'sat_frontends.bridge', 'sat_frontends.quick_frontend', 'sat_frontends.jp',
                'sat_frontends.primitivus', 'sat_frontends.wix', 'sat_frontends.tools', 'sat.stdui', 'twisted.plugins'],
      package_data={'sat': ['sat.sh'],
                    'sat_frontends': ['wix/COPYING']},
      data_files=[(os.path.join(sys.prefix, 'share/locale/fr/LC_MESSAGES'), ['i18n/fr/LC_MESSAGES/sat.mo']),
                  ('share/doc/%s' % NAME, ['CHANGELOG', 'COPYING', 'INSTALL', 'README', 'README4TRANSLATORS']),
                  (os.path.join('share', DBUS_DIR), (DBUS_FILE,)),
                  ],
      scripts=['frontends/src/jp/jp', 'frontends/src/primitivus/primitivus', 'frontends/src/wix/wix'],
      zip_safe=False,
      dependency_links=['http://www.blarg.net/%7Esteveha/pyfeed-0.7.4.tar.gz', 'http://www.blarg.net/%7Esteveha/xe-0.7.4.tar.gz'],
      install_requires=['twisted', 'wokkel >= 0.7.1', 'progressbar', 'urwid >= 1.2.0', 'urwid-satext >= 0.3.0', 'pyfeed', 'xe', 'mutagen', 'pillow', 'lxml', 'pyxdg', 'markdown', 'html2text', 'pycrypto >= 2.6.1', 'python-potr'],
      cmdclass={'install': CustomInstall},
      )  # XXX: wxpython doesn't work, it's managed with preinstall_check
