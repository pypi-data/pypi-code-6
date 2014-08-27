#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


module_path = os.path.join(os.path.dirname(__file__), 'jinja2_stl', '__init__.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version__')][0]
__version__ = eval(version_line.split('__version__ = ')[-1])

readme = open('README.rst').read()
# doclink = """
# Documentation
# -------------

# The full documentation is at http://jinja2_stl.rtfd.org."""
doclink = ''
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='jinja2_stl',
    version=__version__,
    description='A Filestorage template loader for Jinja2.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Jindřich Smitka',
    author_email='smitka.j@gmail.com',
    url='https://github.com/s-m-i-t-a/jinja2_stl',
    packages=[
        'jinja2_stl',
    ],
    package_dir={'jinja2_stl': 'jinja2_stl'},
    include_package_data=True,
    install_requires=[
        'Jinja2>=2.7',
        'six>=1.7.3',
    ],
    license='MIT',
    zip_safe=False,
    keywords='jinja2_stl',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
