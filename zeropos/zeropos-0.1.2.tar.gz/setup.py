#!/usr/bin/env python
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


PACKAGE, VERSION, LICENSE, WEBSITE = None, None, None, None
execfile(os.path.join('zeropos', 'version.py'))


setup(
    name=PACKAGE,
    version=VERSION,
    description=read('README.rst'),
    author="Openlabs Technologies and Consulting (P) Ltd.",
    author_email='info@openlabs.co.in',
    url=WEBSITE,
    package_dir={
        'zeropos': 'zeropos',
    },
    packages=['zeropos'],
    package_data={
        'zeropos': [
            'templates/*.html',
            'static/*',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Tryton',
        'Topic :: Office/Business',
    ],
    license=LICENSE,
    install_requires=[
        'zeroconf',
        'python-escpos',
        'flask',
        'gevent',
    ],
    zip_safe=False,
    scripts=['bin/zeroposd'],
)
