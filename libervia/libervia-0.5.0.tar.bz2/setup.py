#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Libervia: a Salut à Toi frontend
# Copyright (C) 2011, 2012, 2013, 2014  Jérôme Poisson (goffi@goffi.org)
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

from distribute_setup import use_setuptools
use_setuptools()
from setuptools.command.install import install
from setuptools import setup
from distutils.file_util import copy_file
import os
import sys
import subprocess
from stat import ST_MODE
import shutil
from src.server.constants import Const as C

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


NAME = 'libervia'
LAUNCH_DAEMON_COMMAND = 'libervia'

ENV_LIBERVIA_INSTALL = "LIBERVIA_INSTALL"  # environment variable to customise installation
NO_PREINSTALL_OPT = 'nopreinstall'  # skip all preinstallation checks
AUTO_DEB_OPT = 'autodeb'  # automaticaly install debs
CLEAN_OPT = 'clean'  # remove previous installation directories
PURGE_OPT = 'purge'  # remove building and previous installation directories


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

    def custom_auto_options(self):
        """Change options for twistd in the shell script
        Mainly change the paths"""
        sh_buffer = ""
        with open(self.sh_script_path, 'r') as sh_file:
            for ori_line in sh_file:
                if ori_line.startswith('PLUGIN_OPTIONS='):
                    dest_line = 'PLUGIN_OPTIONS="-d %s"\n' % self.install_data_dir
                elif ori_line.startswith('PYTHON='):
                    dest_line = 'PYTHON="%s"\n' % sys.executable
                else:
                    dest_line = ori_line
                sh_buffer += dest_line

        with open(self.sh_script_path, 'w') as sh_file:
            sh_file.write(sh_buffer)

    def custom_create_links(self):
        """Create symbolic links to executables"""
        # the script which launch the daemon
        for source, dest in self.sh_script_links:
            if os.path.islink(dest) and os.readlink(dest) != source:
                os.remove(dest)  # copy_file doesn't force the link update
            dest_name, copied = copy_file(source, dest, link='sym')
            assert (copied)
            # we change the perm in the same way as in the original install_scripts
            mode = ((os.stat(dest_name)[ST_MODE]) | 0555) & 07777
            os.chmod(dest_name, mode)

    def pyjs_build(self):
        """Build the browser side JS files from Python source."""
        cwd = os.getcwd()
        os.chdir(os.path.join('src', 'browser'))
        result = subprocess.call('pyjsbuild libervia_main --no-compile-inplace -I %s -o %s' %
                                 (self.install_lib, self.pyjamas_output_dir), shell=True)
        os.chdir(cwd)
        return result

    def copy_data_files(self):
        # XXX: To copy the JS files couldn't be done with the data_files parameter
        # of setuptools.setup because all the files to be copied must exist before
        # the call. Also, we need the value of self.install_lib to build the JS
        # files (it's not easily predictable as it may vary from one system to
        # another), so we can't call pyjsbuild before setuptools.setup.

        html = os.path.join(self.install_data_dir, C.HTML_DIR)
        if os.path.isdir(html):
            shutil.rmtree(html, ignore_errors=True)
        shutil.copytree(self.pyjamas_output_dir, html)

    def run(self):
        self.sh_script_path = os.path.join(self.install_lib, NAME, 'libervia.sh')
        self.sh_script_links = [(self.sh_script_path, os.path.join(self.install_scripts, LAUNCH_DAEMON_COMMAND))]
        self.install_data_dir = os.path.join(self.install_data, 'share', NAME)
        self.pyjamas_output_dir = os.path.join(os.getcwd(), 'html')
        sys.stdout.write('running pre installation stuff\n')
        sys.stdout.flush()
        if PURGE_OPT in install_opt:
            self.purge()
        elif CLEAN_OPT in install_opt:
            self.clean()
        install.run(self)
        sys.stdout.write('running post installation stuff\n')
        sys.stdout.flush()
        build_result = self.pyjs_build()  # build after libervia.common is accessible
        if build_result == 127:  # TODO: remove magic string
            print "pyjsbuild is not installed or not accessible from the PATH of user '%s'" % os.getenv('USERNAME')
            return
        if build_result != 0:
            print "pyjsbuild failed to build libervia"
            return
        self.copy_data_files()
        self.custom_auto_options()
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
                     self.install_data_dir,
                     os.path.join(self.install_data, 'share', 'doc', NAME),
                     os.path.join(self.install_lib, "%s.egg-info" % self.config_vars['dist_fullname']),
                     os.path.join(self.install_lib, "%s-py%s.egg-info" % (self.config_vars['dist_fullname'], self.config_vars['py_version_short'])),
                     ]:
            if os.path.isdir(path):
                to_remove.append(path)
        for source, dest in self.sh_script_links:
            if os.path.islink(dest):
                to_remove.append(dest)
        plugin_file = os.path.join(self.install_lib, 'twisted', 'plugins', NAME)
        if os.path.isfile(plugin_file):
            to_remove.append(plugin_file)

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
        to_remove = [os.path.join(os.getcwd(), 'build'), self.pyjamas_output_dir]
        self.clean(message, to_remove)


def preinstall_check(install_opt):
    """Check presence of problematic dependencies, and try to install them with package manager
    This ugly stuff is necessary as distributions are not installed correctly with setuptools/distribute
    Hope to remove this at some point"""

    modules_tocheck = []  # if empty this method is dummy

    package = {'twisted': 'python-twisted-core',
               'twisted.words': 'python-twisted-words',
               'twisted.web': 'python-twisted-web',
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
    install_opt = os.environ.get(ENV_LIBERVIA_INSTALL, "").split()
    if not NO_PREINSTALL_OPT in install_opt:  # user can force preinstall skipping
        preinstall_check(install_opt)

setup(name=NAME,
      version='0.5.0',
      description=u'Web frontend for Salut à Toi',
      long_description=u'Libervia is a web frontend for Salut à Toi (SàT), a multi-frontends and multi-purposes XMPP client.',
      author='Association « Salut à Toi »',
      author_email='contact@goffi.org',
      url='http://www.salut-a-toi.org',
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Twisted',
                   'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                   'Operating System :: POSIX :: Linux',
                   'Topic :: Communications :: Chat'],
      package_dir={'libervia': 'src', 'twisted.plugins': 'src/twisted/plugins'},
      packages=['libervia', 'libervia.common', 'libervia.server', 'twisted.plugins'],
      package_data={'libervia': ['libervia.sh']},
      data_files=[(os.path.join('share', 'doc', NAME), ['COPYING', 'README', 'INSTALL']),
                  (os.path.join('share', NAME, C.SERVER_CSS_DIR), [os.path.join(C.SERVER_CSS_DIR, filename) for filename in os.listdir(C.SERVER_CSS_DIR)]),
                  ],
      scripts=[],
      zip_safe=False,
      dependency_links=['http://www.blarg.net/%7Esteveha/pyfeed-0.7.4.tar.gz', 'http://www.blarg.net/%7Esteveha/xe-0.7.4.tar.gz'],
      install_requires=['sat', 'twisted', 'pyfeed', 'xe', 'txJSON-RPC', 'zope.interface', 'pyopenssl'],
      cmdclass={'install': CustomInstall},
      )
