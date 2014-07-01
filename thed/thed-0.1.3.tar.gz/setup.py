from __future__ import unicode_literals

import os
import re
import setuptools

version = (
    re
    .compile(r".*__version__ = '(.*?)'", re.S)
    .match(open('thed/__init__.py').read())
    .group(1)
)

packages = [
    str(s) for s in
    setuptools.find_packages('.', exclude=('tests', 'tests.*'))
]

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid==1.5.1',
    'SQLAlchemy==0.9.6',
    'click==2.2',
    'pilo>=0.3.2,<0.4'
]

extras_require = {
    'tests': [
        'nose>=1.3,<1.4',
        'mock>=1.0,<1.1',
        'ipdb',
        'pyflakes',
        'webtest',
        'WSGIProxy2',
    ]
}

scripts = [
    'bin/thed',
]


setuptools.setup(
    name='thed',
    version=version,
    description='thed',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Balanced',
    author_email='dev+thed@balancedpayments.com',
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    scripts=scripts,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    test_suite='nose.collector',
    entry_points="""\
        [pyramid.scaffold]
        api=thed.scaffolds:APITemplate
      """
)
