#!/usr/bin/env python
# -*- coding:utf-8 -*-

# (c)Ing. Zdenek Dlauhy, Michal Dlauhý, pripravto.cz

"""

Ansiblator - makes Ansible api more pythonic

basic usage::

    from ansiblator.api import Ansiblator
    ans = Ansiblator()
    ret = ans.local("uname -a", now=True, use_shell=True)
    ans.run("uname -a", now=True)
    ans.runner("uptime")
    ans.run_all()
    ans.copy(src="/tmp/aabc.csv", dest="/tmp/",pattern="pc",now=True)

"""

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup
    from distutils.core import Command

import subprocess
import time
import os
import ansiblator.api as an


class upload_pkg(Command):
    description = 'makes test, sets version and uploads to pypi'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def make_revision_py(self):
        os.chdir("{}/ansiblator/".format(os.getcwd()))
        try:
            __revision__ = int(subprocess.check_output(['bzr', 'revno'])[0:-1])
        except Exception as e:
            print(e)
            __revision__ = "0"
        with open("version.py", 'w') as writer:
            timestamp = time.strftime("%d-%m-%Y", time.localtime())
            writer.write("__version__='{}--{}'".format(__revision__, timestamp))
            writer.close()
        print("New revision {}".format(__revision__))

    def save_doc(self, data):
        with open("README.txt", 'w') as writer:
            data = data.replace("\n    ", "\n")
            for line in data:
                writer.write(line)
            writer.close()

    def run(self):
        ansible_file = "ansible_hosts"
        cur_dir = os.getcwd()
        print("Actual directory {}".format(os.getcwd()))
        self.make_revision_py()
        os.chdir(cur_dir)
        ans = an.Ansiblator(inventory=ansible_file, pattern="test", run_at_once=True, use_shell=True, stop_on_error=True)
        self.save_doc(an.Ansiblator.__doc__)
        ans.local('bzr clean-tree --force')
        ans.local('python setup.py clean')
        ans.local('python setup.py test')
        ans.local('python setup.py sdist upload')
        ans.local('python setup.py clean')
        ans.local('bzr clean-tree --force')


if __name__ == "__main__" :
    cmdclass = {'upload_pkg': upload_pkg}
    setup(
      name=an.__sys_name__,
      packages=["ansiblator"],
      version=an.__version__,
      description=an.__desc__,
      author=an.__author__,
      author_email=an.__email__,
      long_description=an.__description__,
      license=an.__license__,
      package_data={'ansiblator':['LICENSE.txt']},
      url=an.__url__,
      keywords=['ansible', 'wrapper', 'automatization', 'api'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
      test_suite="test",
      install_requires=["ansible"],
      cmdclass=cmdclass)
