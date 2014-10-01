# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

long_description = '\n'.join([
    open(os.path.join(".", "README.rst")).read(),
    open(os.path.join(".", "AUTHORS.rst")).read(),
    open(os.path.join(".", "HISTORY.rst")).read(),
])

requires = ['Sphinx>=1.2']

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Documentation',
    'Topic :: Utilities',
]

setup(
    name='sphinxcontrib-gravatar',
    version='0.1.0',
    url='https://github.com/tell-k/sphinxcontrib-gravatar',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-gravatar',
    license='BSD',
    author='tell-k',
    author_email='ffk2005 at gmail.com',
    description='Sphinx "gravatar" extension',
    long_description=long_description,
    zip_safe=False,
    classifiers=classifiers,
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
