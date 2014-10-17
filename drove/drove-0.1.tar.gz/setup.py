#!/usr/bin/env python

import drove as project

import glob
from setuptools import setup
from setuptools import find_packages


def get_file_content(fname):
    try:
        return open(fname).read()
    except:
        return None


setup(
    name=project.NAME,
    version=project.VERSION,
    description=project.DESCRIPTION,
    long_description=get_file_content('README.md'),
    author=project.AUTHOR_NAME,
    author_email=project.AUTHOR_EMAIL,
    url=project.URL,
    packages=find_packages(),
    tests_require=["nose==1.3.3"],
    install_requires=["six>=1.8.0"],
    package_data={
        project.NAME: glob.glob('config/*') + glob.glob('config/plugins/*')
    },
    license=project.LICENSE,
    entry_points={
        'console_scripts': [
            '%s = %s.script:cli' % (project.NAME, project.NAME,),
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],

    test_suite="nose.collector",
    include_package_data=True,
)
