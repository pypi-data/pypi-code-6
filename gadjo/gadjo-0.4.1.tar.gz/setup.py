#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import re
from distutils.command.sdist import sdist
from setuptools import setup, find_packages

class eo_sdist(sdist):

    def run(self):
        print "creating VERSION file"
        if os.path.exists('VERSION'):
            os.remove('VERSION')
        version = get_version()
        version_file = open('VERSION', 'w')
        version_file.write(version)
        version_file.close()
        sdist.run(self)
        print "removing VERSION file"
        if os.path.exists('VERSION'):
            os.remove('VERSION')

def get_version():

    version = None
    for d in glob.glob('*'):
        if not os.path.isdir(d):
            continue
        module_file = os.path.join(d, '__init__.py')
        if not os.path.exists(module_file):
            continue
        for v in re.findall("""__version__ *= *['"](.*)['"]""",
                open(module_file).read()):
            assert version is None
            version = v
        if version:
            break
    assert version is not None
    if os.path.exists('.git'):
        import subprocess
        p = subprocess.Popen(['git','describe','--dirty','--match=v*'],
                stdout=subprocess.PIPE)
        result = p.communicate()[0]
        assert p.returncode == 0, 'git returned non-zero'
        new_version = result.split()[0][1:]
        assert new_version.split('-')[0] == version, '__version__ must match the last git annotated tag'
        version = new_version.replace('-', '.')
    return version


setup(
    name='gadjo',
    version=get_version(),
    description='Django base template tailored for management interfaces',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
    author='Frederic Peters',
    author_email='fpeters@entrouvert.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'XStatic',
        'XStatic_Font_Awesome',
        'XStatic_jQuery',
        'XStatic_jquery_ui',
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
    zip_safe=False,
    cmdclass={
        'sdist': eo_sdist
    },
)
