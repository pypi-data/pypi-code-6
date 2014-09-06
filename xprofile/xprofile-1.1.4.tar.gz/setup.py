# -*- coding: utf-8 -*-
import re
import codecs
from setuptools import setup, Command


class ManCommand(Command):
    description = 'generate man pages'
    user_options = []

    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        print(self)
        print('hoi')

setup(
    name = 'xprofile',
    description = 'A tool to manage and automatically apply xrandr configurations.',
    version = re.search(r'''^__version__\s*=\s*["'](.*)["']''', open('xprofile/__init__.py').read(), re.M).group(1),
    author = 'Nico Di Rocco',
    author_email = 'dirocco.nico@gmail.com',
    url = 'https://github.com/nrocco/xprofile',
    license = 'LICENSE',
    long_description = codecs.open('README.rst', 'rb', 'utf-8').read(),
    test_suite='nose.collector',
    install_requires = [
        'docutils>=0.12'
    ],
    tests_require = [
        'nose',
        'mock',
    ],
    packages = [
        'xprofile'
    ],
    entry_points = {
        'console_scripts': [
            'xprofile = xprofile.__main__:main'
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Desktop Environment',
        'Topic :: Utilities'
    ],
    cmdclass={
        'man': ManCommand
    }
)
