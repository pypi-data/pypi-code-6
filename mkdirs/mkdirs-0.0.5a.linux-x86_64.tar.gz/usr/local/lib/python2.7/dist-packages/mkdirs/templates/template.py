TEMPLATE_MAIN = """import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class {modulename}(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super({modulename}, self).__init__(
            description='{modulename}',
            version='0.1',
            command_manager=CommandManager('{modulename_lower}.app')
        )

    def initialize_app(self, argv):
        self.log.debug('initialize app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = {modulename}()
    return myapp.run(argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
"""

TEMPLATE_SETUP = """PROJECT = '{projectname}'

# Change docs/sphinx/conf.py too!
VERSION = '0.0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description=PROJECT,
    long_description=long_description,

    author='{authorname}',
    author_email='{email}',

    url='https://github.com/{authorname}/{projectname}',
    download_url='https://github.com/{authorname}/{projectname}',


    # 1.2.0.dev1  # Development release
    # 1.2.0 a1     # Alpha Release
    # 1.2.0b1     # Beta Release
    # 1.2.0rc1    # RC Release
    # 1.2.0       # Final Release
    # 1.2.0.post1 # Post Release

    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Build Tools',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    keywords='sample setuptools development',

    platforms=['Any'],
    scripts=[],
    provides=[],
    install_requires=['cliff'],
    namespace_packages=[],
    packages=find_packages(exclude=['']),
    include_package_data=True,
"""

TEMPLATE_SETUP_CFG = """[metadata]
name = {projectname}
description-file = README.rst
author = James Beedy
author-email = jamesbeedy@gmail.com
summary = {projectname}
home-page = https://githup.com/projectname
classifier =
    Development Status :: 3 - Alpha
    License :: OSI Approved :: Apache Software License
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.2
    Programming Language :: Python :: 3.3
    Intended Audience :: Developers
    Environment :: Console

keywords = 
    sample 
    setuptools 
    development

platforms =
    Any

install_requires = 
    cliff

namespace_packages=[]

packages = 
    find_packages(exclude=[''])

include_package_data=True

[files]
packages =
    {modulename}

[entry_points]
console_scripts =
    {modulename} = {modulename}.main:main

{modulename}.app =
    #simple = {modulename}.simple:Simple

[build_sphinx]
all_files = 1
build-dir = docs/build
source-dir = docs/source


"""
