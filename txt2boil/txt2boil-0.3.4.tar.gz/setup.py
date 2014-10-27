#!/usr/bin/python

from setuptools import *
from distutils.errors import DistutilsError
import os
import glob
from txt2boil.version import version


class total_upload(Command):

    description = "upload all available binaries"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    commands = ['register', 
                'sdist',
                'bdist_rpm',
                'bdist_msi', 'bdist_msi_fixed',
                'bdist_egg',
                'upload']

    def run(self):
        for c in self.commands:
            try:
                self.run_command(c)
            except DistutilsError:
                pass


with open(glob.glob('README.*')[0]) as f:
    long_description = f.read()

setup(
    name='txt2boil', license='MIT', version=version,

    description='A configurable boilerplate generator.',
    long_description=long_description,

    author='Kieran Colford', author_email='colfordk@gmail.com',
    maintainer='Kieran Colford', maintainer_email='colfordk@gmail.com',

    url='https://github.com/kcolford/txt2boil',
    download_url='',            # TODO

    packages=find_packages(),
    test_suite='txt2boil.test',
    entry_points={'console_scripts':['txt2boil = txt2boil.main:main']},

    platforms=['Any'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Code Generators',
    ],

    use_2to3=True,

    cmdclass={'total_upload':total_upload},

    setup_requires=['xdistutils'],
)
