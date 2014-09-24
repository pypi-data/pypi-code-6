# -*- codeing: utf-8 -*-
"""
    setup
    ~~~~~

    distutils control file
"""

readme = open('README.rst').read()

from distutils.core import setup, Command

class PyTest(Command):
    user_options=[]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


import pylit6.__about__ as about

setup(
    name=about.__title__,
    version=about.__version__,
    author=about.__author__,
    author_email=about.__email__,
    url=about.__url__,
    description=about.__summary__,
    long_description=readme,
    license=about.__license__,
    scripts = ['scripts/pylit6'],
    packages = ['pylit6'],
)

